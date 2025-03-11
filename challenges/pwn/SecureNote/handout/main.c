#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* (*read_note)(char*);
    void (*show_note)(char*);
    void (*edit_note)(char*);
    void (*exit_note)(char*);
} NoteVTable;


void setup() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}

char* read_note(char *note_content) {
    if (note_content != NULL) {
        printf("Note already exists! You can only read once.\n");
        return note_content;
    }

    note_content = malloc(100);
    if (note_content == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }

    printf("Enter note: ");
    fgets(note_content, 100, stdin);
    note_content[strcspn(note_content, "\n")] = '\0';
    return note_content;
}

void show_note(char* note_content) {
    if (note_content == NULL) {
        printf("No note exists! Read a note first.\n");
        return;
    }
    printf("Your note: ");
    printf(note_content);
}

void edit_note(char* note_content) {
    if (note_content == NULL) {
        printf("No note exists! Read a note first.\n");
        return;
    }
    printf("Edit note: ");
    fgets(note_content, 100, stdin);
    note_content[strcspn(note_content, "\n")] = '\0';
}

void exit_note(char* note_content) {
    printf("Exiting...\n");
    free(note_content);
    exit(0);
}

int challenge() {
    char *note_content = NULL;
    
    NoteVTable vtable = { 
        .read_note = read_note,
        .show_note = show_note,
        .edit_note = edit_note,
        .exit_note = exit_note
    };

    while (1) {
        printf("\n[SecureNote Menu]\n");
        printf("1. Read note\n");
        printf("2. Show note\n");
        printf("3. Edit note\n");
        printf("4. Exit\n");
        printf("> ");

        int choice;
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input!\n");
            while (getchar() != '\n');
            continue;
        }
        getchar();

        switch (choice) {
            case 1:
                note_content = vtable.read_note(note_content);
                break;
            case 2:
                vtable.show_note(note_content);
                break;
            case 3:
                vtable.edit_note(note_content);
                break;
            case 4:
                vtable.exit_note(note_content);
                break;
            default:
                printf("Invalid choice!\n");
        }
    }
    return 0;
}

int main() {
    setup();
    challenge();
    return 0;
}
