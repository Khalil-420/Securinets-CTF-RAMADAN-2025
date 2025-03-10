#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct string {
    unsigned length;
    char *data;
} string;

void hacked() {
    
    system("/bin/sh");  
}

int main() {
    string *s = malloc(sizeof(string));  
    if (s == NULL) {
        perror("malloc failed");
        return 1;
    }

    puts("welcome patrick ");
    scanf("%u", &s->length);

    s->data = malloc(s->length + 1);
    if (s->data == NULL) {
        perror("malloc failed");
        return 1;
    }
    memset(s->data, 0, s->length + 1);

    puts("Enter something");
    read(0, s->data, s->length);

    free(s->data);  
    free(s);        

    char *s2 = malloc(16);  
    if (s2 == NULL) {
        perror("malloc failed");
        return 1;
    }
    memset(s2, 0, 16);

    puts("Enter more");
    read(0, s2, 15);

    printf("well?\n");
    s->data = (char*)hacked;  

    puts("oh no");
    puts(s->data);  

    free(s2);

    return 0;
}

