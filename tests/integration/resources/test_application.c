#include <time.h>

void my_sleep(){
    int milisec = 100; // length of time to sleep, in miliseconds
    struct timespec req = {0};
    req.tv_sec = 0;
    req.tv_nsec = milisec * 1000000L;
    nanosleep(&req, (struct timespec *)NULL);
}

void func1(char * param1, char * param2)
{
    my_sleep();
}

void func2(int param)
{
    my_sleep();
}

void func3()
{
    my_sleep();
}

void func4()
{
    func2(3);
    func3();
    func3();
    func3();
    func3();
    func3();
}

void func5()
{
    func1("param1", "param2");
    func1("param3", "param4");
}

void func6()
{
    func4();
    func5();
}

int main(int argc, char * argv[])
{
    func6();
    return 0 ;
}

