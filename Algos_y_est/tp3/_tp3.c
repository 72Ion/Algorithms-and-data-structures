
#include "tp3.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct dictionary {
  destroy_f destroy;
  size_t quantity;
  size_t array_size;
  struct node **array;
} dictionary_t;

struct node {
  char *key;
  void *value;
  struct node *next;
};

char *my_strdup(const char *s) {
  size_t len = strlen(s) + 1;
  char *copy = malloc(len);
  if (!copy) return NULL;
  memcpy(copy, s, len);
  return copy;
}

long unsigned int hash_function(const char *key) {
  long unsigned int hash = 0;
  int i = 0;
  while (key[i] != '\0') {
    hash = hash * 31 + key[i];
    i++;
  }
  return hash;
}


void rehash_dictionary(dictionary_t *dictionary) {
  if (!dictionary) return;

  size_t new_size = dictionary->array_size * 2;
  struct node **new_array = calloc(new_size, sizeof(struct node *));
  if (!new_array) return;

  for (size_t i = 0; i < dictionary->array_size; i++) {
    struct node *current = dictionary->array[i];
    while (current != NULL) {
      struct node *next = current->next;
      long unsigned int hash = hash_function(current->key) % new_size;
      current->next = new_array[hash];
      new_array[hash] = current;
      current = next;
    }
  }

  free(dictionary->array);
  dictionary->array = new_array;
  dictionary->array_size = new_size;
}


dictionary_t *dictionary_create(destroy_f destroy) {
  dictionary_t *dictionary = malloc(sizeof(dictionary_t));
  if (!dictionary) return NULL;
  dictionary->destroy = destroy;
  dictionary->array_size = 10; 
  dictionary->quantity = 0;
  dictionary->array = calloc(dictionary->array_size, sizeof(struct node*));
  if (!dictionary->array) {
    free(dictionary);
    return NULL;
  }
  return dictionary;
}

void dictionary_destroy(dictionary_t *dictionary) {
    if (!dictionary) return;
    for (size_t i = 0; i < dictionary->array_size; i++) {
        struct node *current = dictionary->array[i];
        while (current != NULL) {
            struct node *next = current->next;
            free(current->key);
            if (dictionary->destroy && current->value) dictionary->destroy(current->value);
            free(current);
            current = next;
        }
    }
    free(dictionary->array);
    free(dictionary);
}

bool dictionary_put(dictionary_t *dictionary, const char *key, void *value) { 

  if (!dictionary || !key || strlen(key) <= 0) return false;
  if (dictionary_contains(dictionary, key)) {
    dictionary_delete(dictionary,key);
  }

  float load_factor = (float)dictionary->quantity / (float)dictionary->array_size;
  if (load_factor > 0.7) {
    rehash_dictionary(dictionary);
  }

  long unsigned int hash = hash_function(key) % dictionary->array_size;
  struct node *new_node = malloc(sizeof(struct node));
  if (!new_node) return false;

  new_node->key = my_strdup(key);
  new_node->value = value;
  new_node->next = dictionary->array[hash];
  dictionary->array[hash] = new_node;
  dictionary->quantity++;
  return true;
}

void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err) {
  if (!dictionary_contains(dictionary, key)) {
    *err = true;
    return NULL;
  }
  long unsigned int hash = hash_function(key) % dictionary->array_size;
  if (dictionary->array[hash] != NULL) {
    struct node *current = dictionary->array[hash];
    while (current != NULL) {
      if (strcmp(current->key, key) == 0) {
        *err = false;
        return current->value;
      }
      current = current->next;
    }
  }

  return NULL;
}
bool dictionary_delete(dictionary_t *dictionary, const char *key) {
    if (!dictionary_contains(dictionary, key)) return false;
    long unsigned int hash = hash_function(key) % dictionary->array_size;
    struct node *current = dictionary->array[hash];
    struct node *prev = NULL;

    while (current != NULL && strcmp(current->key, key) != 0) {
        prev = current;
        current = current->next;
    }

    if (prev == NULL) {
        dictionary->array[hash] = current->next;
    } else {
        prev->next = current->next;
    }
    if (dictionary->destroy && current->value) dictionary->destroy(current->value);
    free(current->key);
    current->key = NULL;
    current->value = NULL;
    free(current);
    dictionary->quantity--;
    return true;
}

void *dictionary_pop(dictionary_t *dictionary, const char *key, bool *err) {
  if (!dictionary_contains(dictionary, key)) {
    *err = true;
    return NULL;
  }
  void *value = dictionary_get(dictionary, key, err);
  *err = false;
  long unsigned int hash = hash_function(key) % dictionary->array_size;
    struct node *current = dictionary->array[hash];
    struct node *prev = NULL;

    while (current != NULL && strcmp(current->key, key) != 0) {
        prev = current;
        current = current->next;
    }

    if (prev == NULL) {
        dictionary->array[hash] = current->next;
    } else {
        prev->next = current->next;
    }
    free(current->key);
    current->key = NULL;
    current->value = NULL;
    free(current);
    dictionary->quantity--;
  return value;
}

bool dictionary_contains(dictionary_t *dictionary, const char *key) {
  if (!dictionary || !key || strlen(key) <= 0) return false;
  long unsigned int hash = hash_function(key) % dictionary->array_size;
  struct node *current = dictionary->array[hash];
  while (current != NULL) {
    if (strcmp(current->key, key) == 0) {
      return true;
    }
    current = current->next;
  }
  return false;
}

size_t dictionary_size(dictionary_t *dictionary) {
  if (!dictionary) return 0;
  return dictionary->quantity;
}

