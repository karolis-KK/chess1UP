#include <iostream>
#include <fstream>

using namespace std;

void funkc(int isvis, int &po_5, int &po_2, int &po_1) {
    while (true) {
            if (isvis - 5 < 0) {
                break;
            }
            isvis -= 5;
            po_5++;
        }
    while (true) {
            if (isvis - 2 < 0) {
                break;
            }
            isvis -= 2;
            po_2++;
        }
    while (true) {
            if (isvis - 1 < 0) {
                break;
            }
            isvis -= 1;
            po_1++;
        }
}

int main() {
    int n, isvis, po_5 = 0, po_2 = 0, po_1 = 0;
    
    ifstream FD("Duomenys.txt");
    ofstream FR("Rezultatas.txt");

    FD >> n;

    for (int i = 0; i < 3; i++) {
        FD >> isvis;
        funkc(isvis, po_5, po_2, po_1);
        FR << po_5 << " " << po_2 << " " << po_1 << endl;
        po_5 = 0;
        po_2 = 0;
        po_1 = 0;
    }

    FR.close();
    FD.close();
}