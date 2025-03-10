#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void love_and_water() {
    printf("Two lovers wander down to the shore\n");
    printf("Hand in hand the evening before\n");
    printf("The day that their hands will be joined\n");
    printf("She enters and swims with the foam\n");
    printf("He bids her come out and come home\n");
    printf("But deeper and colder she goes\n");
}

void wedding_bed() {
    printf("The silt of our wedding bed\n");
    printf("The pebbles where you lay your head\n");
    printf("Love, come in, the water is fine\n");
    printf("When she is pulled beneath the rush\n");
    printf("He waits and waves, his face aflush\n");
    printf("'Til the pale imitation drifts up\n");
}

void river_sickness() {
    printf("The minnows our witnesses\n");
    printf("The cause of our sickness is\n");
    printf("Love, come in, the water is fine\n");
    printf("Blood runs thicker than water\n");
    printf("Blood runs thicker than water\n");
    printf("But both feel the same when your eyes are closed\n");
}

void river_daughter() {
    printf("I am the river's daughter\n");
    printf("I am the river's daughter\n");
    printf("I am the river's daughter\n");
    printf("And you'll be her son when we're both reposed\n");
    printf("Blood runs thicker than water\n");
    printf("But both feel the same when your eyes are closed\n");
}

void secret_function() {
    printf("Thank you\n");
    system("/bin/sh");  
}

void vuln(char *input) {
    char buffer[64];
    strcpy(buffer, input);  
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_string>\n", argv[0]);
        return 1;
    }

    love_and_water();
    wedding_bed();
    river_sickness();
    river_daughter();

  
    vuln(argv[1]);

    printf("Program finished successfully.\n");
    return 0;
}

