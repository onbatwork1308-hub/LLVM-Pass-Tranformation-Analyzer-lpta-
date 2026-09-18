#define CONST 10
int atoi(char* a) {
    int i = 0;
    for(int j = 0; a[j] != '\0'; j++) {
        i = i * 10 + (a[j] - '0');
    }

    return i;
}

int main(int argc, char* argv[]) {
    int a = 0;
    if(argc == 0) {
        for(int i = 0; i < 10; i++) {
            a++;
        }
    }
    else if(argc == 1){
        int c = atoi(argv[argc]);
        for(int i = 0; i < c; i++) {
            a++;
        }
    }

    return a;
}

