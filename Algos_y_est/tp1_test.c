#include "tp1.h"
#include <stdlib.h>

bool is_prime(int x){

    /**
    * Verifica la propiedad de un numero para ver si es primo
    * Parametros: 
    *   x - El int que se quiere verificar
    * Returns:
    *   Valor Bool 1 en true y 0 en false para calificar de si primo o no primo al int x.
    * Ejemplos:
    *   bool result1 = is_prime(23) // result1 es ahora 1
    *   bool result2 = is_prime(65) // result2 es ahora 0
    **/

    int prime_case = 0;
    int i;

    if (x == 2) {
        return true;
    }

    for (i = 3; i < x; i+=2) {
        if (x % i == 0) {
            prime_case += 1;
            if (prime_case) {
                return false;
            }
        }
    }
    return true;
}

int storage_capacity(float d, float v){

    /**
    * Devuelve la cantidad de productos que entran en un deposito segun el volumen de un producto y un deposito.
    * Parametros: 
    *   d (float)- Representa el volumen del deposito
    *   v (float)- Representa el volumen de un producto
    * Returns:
    *   result_int (int) - Es la cantidad de productos que entran en el deposito.
    * Ejemplos:
    *   int result1 = storage_capacity(90,9) // result1 es ahora 10
    *   int result2 = storage_capacity(9,90) // result1 es ahora 0
    **/

    int result_int;
    if (v <= 0 || d <= 0) {
        // printf("Porfavor ingrese un volumen de producto y/o deposito apropiado");
        return 0;
    } else {
        float result = d / v;
        result_int = (int)result;
        return result_int;
    }
}

void swap(int *x, int *y) {
    /**
     * Hace el swap de dos valores de int
     * 
     * Parametros: 
     *      x (int*): Un puntero al primer valor x tipo int.
     *      y (int*): Puntero al segundo valor y tipo int.
     * 
     * Returns:
     *      Esta funcion no devuelve un valor.
     * Ejemplo de uso:
     *      int a = 5, b = 10;
     *      swap(&a, &b);
     *      // ahora a es 10 y b es 5 
    **/    
    int temp = *x;
    *x = *y;
    *y = temp;
    return;
}

int array_max(const int *array, int length) {
    // No agregare documentation a partir de esta funcion.
    int valor_max = array[0];
    for (int i = 0; i < length; i++) {
        if (array[i] > valor_max) {
            valor_max = array[i];
        }
    }
    return valor_max;
}

void array_map(int *array, int length, int f(int)) {
    if (!array || !f) return;

    for (int i = 0; i < length; i++) {
        array[i] = f(array[i]);
    }
    return;
}

int *copy_array(const int *array, int length) {
    if (!array) return NULL;
    int* array_copy = malloc(sizeof(int)*length);
    for (int i = 0; i < length; i++) {
        array_copy[i] = array[i]; 
    }
    return array_copy;
}

int **copy_array_of_arrays(const int **array_of_arrays, const int *array_lenghts, int array_amount){
    if (!array_of_arrays || !array_lenghts) return NULL;

    int** copy = malloc(sizeof(int*) * (array_amount));

    for (int i = 0; i<array_amount; i++) {
        if (!array_of_arrays[i]) {
            copy[i] = NULL;
        } else {
            copy[i] = malloc(sizeof(int)*array_lenghts[i]);
            for (int j=0; j < array_lenghts[i]; j++) {
                copy[i][j] = array_of_arrays[i][j];
        }
        }
    }
    return copy;
}

void free_array_of_arrays(int **array_of_arrays, int *array_lenghts, int array_amount){
    for (int i = 0; i < array_amount; i++) {
        free(array_of_arrays[i]);
        }
    free(array_of_arrays);
    free(array_lenghts);
    return;
}

void bubble_sort(int *array, int length){
    if (!array) return;

    bool swap;
    int temp;

    for (int i = 0; i< length-1; i++) {
        swap = false;
        for (int j = 0; j < length-i-1; j++) {
            if (array[j]>array[j+1]) {
                temp = array[j];
                array[j] = array[j+1];
                array[j+1] = temp;
                swap = true;
            }            
        }
        if (!swap) break;
    }
    return;
}

bool array_equal(const int *array1, int length1, const int *array2, int length2) {
    if (!array1 && !array2) return true;
    if ((length1 != length2) || !array1 || !array2) return false;

    for (int i = 0; i < length1; i++) {
        if (array1[i] != array2[i]) {
            return false;
        }
    }
    return true;
}

bool integer_anagrams(const int *array1, int length1,
                      const int *array2, int length2) {
    if (!array1 || !array2) return false;
    if (length1 != length2) return false;
    
    int* array1_cp = copy_array(array1, length1);
    int* array2_cp = copy_array(array2, length2);

    bubble_sort(array1_cp, length1);
    bubble_sort(array2_cp, length2);

    bool bool_val = array_equal(array1_cp, length1, array2_cp, length2);
    
    free(array1_cp);
    free(array2_cp);
    
    return bool_val;
}