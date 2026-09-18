int sum_array(int* arr, int arrSize) {
    int sum = 0;
    for(int i = 0; i < arrSize; i++) {
        sum += arr[i];
    }
    
    return sum;
}