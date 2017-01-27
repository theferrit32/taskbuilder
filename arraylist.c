#include <stdlib.h>
#include <stdio.h>
#include "arraylist.h"

#define INITIAL_CAPACITY 10
#define GROWTH_THRESHOLD 0.8
#define GROWTH_FACTOR 2

typedef struct {
    void **array;
    size_t size;
    size_t capacity;
} arraylist;

static bool ensure_capacity(arraylist *list);

/*headers*/
arraylist *arraylist_new();
void arraylist_init(arraylist **list);

arraylist *
arraylist_new()
{
    printf("arraylist_new\n");
    arraylist *list = malloc(sizeof(arraylist));
    arraylist_init(&list);
    return list;
}

void
arraylist_init(arraylist **list_ptr)
{
    printf("arraylist_init\n");
    arraylist *list = *list_ptr;
    list = calloc(1, sizeof(arraylist));
    list->array = calloc(INITIAL_CAPACITY, sizeof(void*));
    list->size = 0;
    list->capacity = INITIAL_CAPACITY;
    *list_ptr = list;
}

bool
arraylist_add(arraylist *list, void *elem)
{
    printf("arraylist_add\n");
    if (!ensure_capacity(list))
    {
        return false;
    }
    
    list->array[list->size] = elem;
    list->size++;
    
    return true;
}

void *
arraylist_get(arraylist *list, int index)
{
    // TODO error cases
    return list->array[index];
}

size_t
arraylist_size(arraylist *list)
{
    return list->size;
}

static
bool
ensure_capacity(arraylist *list)
{
    printf("ensure_capacity\n");
    if (list != NULL &&
            (double)list->size >= (double)(list->capacity * GROWTH_THRESHOLD))
    {
        printf("reallocing\n");
        void *newArray = realloc(list->array, list->capacity * GROWTH_FACTOR);
        if (newArray)
        {
            printf("realloced\n");
            size_t new_capacity = list->capacity * GROWTH_FACTOR;
            printf("previous capacity: %lu, new capacity: %lu\n", list->capacity, new_capacity);
            list->capacity = new_capacity;
            return true;
        }
        perror("realloc");
    }
    return false;
}

int
main(int argc, char *argv[])
{
    arraylist *list = arraylist_new();
    printf("list capacity: %lu\n", list->capacity);
    
    for (int i = 0; i < 10; i++)
    {
        int *elem = malloc(sizeof(int));
        arraylist_add(list, elem);
    }
}
