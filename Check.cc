#include <cstdio>
#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
using namespace std;

#define input Test_name+num[i]+".in"
#define output Test_name+num[i]+".out"

int main() {
    string Program_name, Test_name;
    cout << "Please Input (Program name, Test name)(a1, a)\n>"; 
    cin >> Program_name >> Test_name;
    int i = 1;
    string num[6] = {"0", "1", "2", "3", "4", "5"};
    for (int j = 0; j <= 6; ++ j) {
        fstream Test_file;
        Test_file.open((Test_name + num[i] + ".in").data(), ios::in);
        if (!Test_file) {
            return printf("Success!\n"), 0;
        } else {
            // ./a1 < a1.in > mu_ans.out
            system(("./" + Program_name + " < " + input + " > my_ans.out").data());
            if (system(("diff -Z -B my_ans.out " + output).data())) {
                printf("WA %d \n", i);
                // break;
            } else printf("AC %d \n", i);
        }
        ++ i;
    }
}
