#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <foothread.h>
#include <sys/time.h>
#include <time.h>

foothread_barrier_t barrier;

// Function to be executed by threads
void *thread_function(void *arg) {
    int thread_id = *((int *)arg);
    printf("Thread %d is executing\n", thread_id);
    sleep(1); // Simulating some work
    printf("Thread %d finished execution\n", thread_id);
    struct timeval current_time;
        gettimeofday(&current_time, NULL);
    printf("current time: %d\n",current_time.tv_sec);
    //foothread_exit();
    return NULL;
}

// Function to be executed by threads for barrier test
void *thread_function_barrier(void *arg) {
    int thread_id = *((int *)arg);
    printf("Thread %d is executing\n", thread_id);
    sleep(1); // Simulating some work
    printf("Thread %d finished execution\n", thread_id);
    foothread_barrier_wait(&barrier);
    return NULL;
}

// Function to be executed by threads with arguments
void *thread_function_with_args(void *arg) {
    char *message = (char *)arg;
    printf("%s\n", message);
    return NULL;
}

int main() {
    // Test foothread_create and foothread_exit
    foothread_t thread1;
    int arg1 = 1;
    printf("Creating thread 1\n");
    foothread_create(&thread1, NULL, thread_function, &arg1);
    sleep(2); // Wait for the thread to finish before exiting

    // Test foothread_attr_setjointype and foothread_attr_setstacksize
    foothread_attr_t attr;
    foothread_attr_setjointype(&attr, FOOTHREAD_JOINABLE);
    foothread_attr_setstacksize(&attr, 1024 * 1024); // 1MB stack size
    foothread_t thread2;
    int arg2 = 2;
    foothread_create(&thread2, &attr, thread_function, &arg2);
    sleep(2); // Wait for the thread to finish before exiting

    // foothread_t thread3;
    // int arg3 = 3;
    // printf("Creating thread 3\n");
    // foothread_create(&thread3, NULL, thread_function, &arg3);

    // sleep(2); // Wait for the thread to finish before exiting

    // foothread_t thread4;
    // int arg4 = 4;
    // printf("Creating thread 4\n");
    // foothread_create(&thread4, NULL, thread_function, &arg4);


    // Test foothread_mutex_init, foothread_mutex_lock, foothread_mutex_unlock, and foothread_mutex_destroy
    foothread_mutex_t mutex;
    foothread_mutex_init(&mutex);
    foothread_mutex_lock(&mutex);
    printf("Inside critical section\n");
    foothread_mutex_unlock(&mutex);
    foothread_mutex_destroy(&mutex);

    sleep(5); // Wait for the threads to finish before exiting

    // Test foothread_barrier_init, foothread_barrier_wait, and foothread_barrier_destroy
    
    foothread_barrier_init(&barrier, 3); // Waiting for 3 threads
    foothread_t thread3, thread4, thread5;
    int arg3 = 3, arg4 = 4, arg5 = 5;
    foothread_create(&thread3, NULL, thread_function_barrier, &arg3);
    //sleep(2); // Wait for the thread to finish before exiting
    foothread_create(&thread4, NULL, thread_function_barrier, &arg4);
    //sleep(2); // Wait for the thread to finish before exiting
    foothread_create(&thread5, NULL, thread_function_barrier, &arg5);
    //sleep(2); // Wait for the thread to finish before exiting
    foothread_barrier_wait(&barrier); // All threads reached barrier
    printf("All threads passed barrier\n");
    foothread_barrier_destroy(&barrier);

    return 0;
}
