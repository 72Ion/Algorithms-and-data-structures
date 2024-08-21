#include "tp2.h"
#include <stdlib.h>
#include <stdbool.h>

struct node;
typedef struct node node_t;

struct node {
    void* value;
    node_t* next;
    node_t* prev;
};

struct list {
    node_t* head;
    node_t* tail;
    size_t size;
};

struct list_iter {
    list_t* list;
    node_t* curr;
};

list_t *list_new(){
    list_t *nueva_lista = (list_t*)malloc(sizeof(list_t));
    if (!nueva_lista) return NULL;
    
    nueva_lista->size = 0;
    nueva_lista->head = NULL;
    nueva_lista->tail = NULL;
    return nueva_lista;
}

size_t list_length(const list_t *list){
    if (!list) return 0;
    return list->size;
}

bool list_is_empty(const list_t *list){
    if (!list) return true;
    return (list->size == 0);
}

bool list_insert_head(list_t *list, void *value) {
    if (!list) 
        return false;
    
    node_t* new_node = (node_t*)malloc(sizeof(node_t));
    if (!new_node) return false;

    new_node->value = value;
    new_node->next = list->head;
    new_node->prev = NULL;

    if (list->head != NULL) {
        list->head->prev = new_node;
    }
    list->head = new_node;

    if (list->size == 0)
        list->tail = new_node;

    list->size++;

    return true;
}


bool list_insert_tail(list_t *list, void *value){
    if (!list) return false;
    
    node_t* new_node = (node_t*)malloc(sizeof(node_t));
    if (!new_node) return false;

    new_node->value = value;
    new_node->next = NULL;

    if (!list->tail) {
        new_node->prev =NULL;
        list->head = new_node;
    } else {
        new_node->prev = list->tail;
        list->tail->next = new_node;
    }

    list->tail = new_node;
    
    if (list->tail==new_node) {
        list->size++;
        return true;
    }

    return false;
}

void *list_peek_head(const list_t *list){
    if (!list) return NULL;
    if (list_is_empty(list)) return NULL;

    return list->head->value;
}

void *list_peek_tail(const list_t *list){
    if (!list) return NULL;
    if (list_is_empty(list)) return NULL;

    return list->tail->value;
}

void *list_pop_head(list_t *list){
    if(!list || !list->head) return NULL;
    node_t* aux = list->head;
    void* value = aux->value;
    list->head = list->head->next;
    if(!list->head) {
        list->tail = NULL;
    } else {
        list->head->prev = NULL;
    }
    free(aux);
    list->size--;
    return value;
}

void *list_pop_tail(list_t *list){
    if (!list ||list_is_empty(list)||list->tail==NULL) return NULL;
    void* value = list->tail->value;
    node_t *temp = list->tail;

    if (list->size==1) {
        list->head=NULL;
        list->tail=NULL;
    } else {
        list->tail = list->tail->prev;
        list->tail->next = NULL;
    }

    free(temp);
    list->size--;
    return value;
}

void list_destroy(list_t *list, void destroy_value(void *)){
    if (!list) return;
    node_t* actual = list->head;
    while(actual!=NULL) {
        node_t* temp = actual;
        actual = actual->next;

        if (destroy_value != NULL) {
            destroy_value(temp->value);
        }

        free(temp);
    }
    free(list);
    return;

}

list_iter_t *list_iter_create_head(list_t *list){
    if (!list) return NULL;
    
    list_iter_t* iterable = (list_iter_t*)malloc(sizeof(list_iter_t));
    if (!iterable) return NULL;

    iterable->list = list;
    iterable->curr = list->head;

    return iterable;
}

list_iter_t *list_iter_create_tail(list_t *list){
    if (!list) return NULL;
    
    list_iter_t* iterable = (list_iter_t*)malloc(sizeof(list_iter_t));
    if (!iterable) return NULL;

    iterable->list = list;
    iterable->curr = list->tail;

    return iterable;
}

bool list_iter_forward(list_iter_t *iter){
    if (!iter || iter->curr == NULL || iter->curr->next == NULL) return false;
    iter->curr = iter->curr->next;
    return true;
}

bool list_iter_backward(list_iter_t *iter){
    if (!iter || iter->curr == NULL || iter->curr->prev == NULL) return false;
    iter->curr = iter->curr->prev;
    return true;
}

void *list_iter_peek_current(const list_iter_t *iter){
    if (!iter||iter->curr == NULL) return NULL;
    return iter->curr->value;
}

bool list_iter_at_last(const list_iter_t *iter){
    if (!iter || !(iter->list)) return false;
    return (list_is_empty(iter->list)||iter->curr == iter->list->tail);
}

bool list_iter_at_first(const list_iter_t *iter){
    if (!iter || !(iter->list)) return false;
    if (list_is_empty(iter->list)||iter->curr == iter->list->head) return true; 
    return false;
}

void list_iter_destroy(list_iter_t *iter){
    if (iter!= NULL) {
        free(iter);
    }
    return;
}

bool list_iter_insert_after(list_iter_t *iter, void *value) {
    if (!iter || !iter->list) return false;

    node_t* new_node = (node_t*)malloc(sizeof(node_t));
    if (!new_node) return false;

    new_node->value = value;
    new_node->next = NULL; 
    new_node->prev = iter->curr;

    if (!iter->curr || !iter->curr->next) {
        if (!iter->list->head) {
            iter->list->head = new_node;
        } else if (iter->curr) {
            iter->curr->next = new_node;
            new_node->prev = iter->curr;
        }
        iter->list->tail = new_node;
        iter->curr = new_node;
    } else { 
        new_node->next = iter->curr->next;
        iter->curr->next->prev = new_node;
        iter->curr->next = new_node;
    }

    iter->list->size++;
    return true;
}

bool list_iter_insert_before(list_iter_t *iter, void *value){
    if (!iter || !value) return false;

    node_t* new_node = (node_t*) malloc(sizeof(node_t));
    if (!new_node) return false;

    new_node->value = value;
    
    if (iter->curr) {
        if (iter->curr->prev) {
            iter->curr->prev->next = new_node;
            new_node->next = iter->curr;
            new_node->prev = iter->curr->prev;
            iter->curr->prev = new_node;
        } else {
            new_node->prev = NULL;
            iter->list->head = new_node;
            new_node->next = iter->curr;
            iter->curr->prev = new_node;
        }
    } else {
        if (!iter->list->tail) {
            iter->list->tail = new_node;
        }
        iter->list->head = new_node;
    }
    iter->list->size++;
    return true;
}


void *list_iter_delete(list_iter_t *iter){
    if (!iter || !iter->list || !iter->curr) return NULL;

    void* val = iter->curr->value;  
    node_t* nodeToDelete = iter->curr;

    if (nodeToDelete == iter->list->head) {
        iter->curr = iter->list->head->next;
        void *poppedValue = list_pop_head(iter->list);
        return poppedValue;
    }

    if (nodeToDelete == iter->list->tail) {
        iter->curr = nodeToDelete->prev;  
        void *poppedValue = list_pop_tail(iter->list);  
        return poppedValue;
    }

    if (nodeToDelete->next) {
        nodeToDelete->next->prev = nodeToDelete->prev;
    }
    if (nodeToDelete->prev) {
        nodeToDelete->prev->next = nodeToDelete->next;
    }

    list_iter_forward(iter);

    iter->list->size--; 
    free(nodeToDelete); 

    return val; 
}
