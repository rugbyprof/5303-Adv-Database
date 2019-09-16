#include <iostream>
#include <fstream>
#include <string>
#include <math.h>

using namespace std;

void loadFile(string filename){
    ofstream fout(filename);

    for(int i = 0;i<7;i++){
        fout<<rand()%1000;
        fout<<endl;
    }
}

int loadArray(int *&a,string fileName){
    ifstream fin(fileName);

    int dummy=0;
    int size=0;

    while (!fin.eof())     
    {
        fin >> dummy;       

        size++;        
    }

    fin.close();

    a = new int[size+1];

    ifstream fin2;           // input file type
    fin2.open(fileName);     // connect fin to our actual file

    for (int i = 0; i < size; i++)
    {
        fin2 >> a[i];
    }

    return size;
}

void printArray(int *a,int size){
    for(int i=0;i<size;i++){
        cout<<a[i]<<" ";
    }
    cout<<endl;
}

void swap(int *xp, int *yp)  
{  
    int temp = *xp;  
    *xp = *yp;  
    *yp = temp;  
}  

void bubbleSort(int arr[], int n)  
{  
    int i, j;  
    for (i = 0; i < n-1; i++)     
      
    // Last i elements are already in place  
    for (j = 0; j < n-i-1; j++)  
        if (arr[j] > arr[j+1])  
            swap(&arr[j], &arr[j+1]);  
}

void binaryLoad(int arr[],int left,int right,int *arr2,int index){
   cout<<left<<":"<<right<<endl;
    if(left == right || index > 7){
        return;
    }

    int mid = floor(left+right / 2);
    arr2[index] = arr[mid];
    
    binaryLoad(arr,left,mid,arr2,++index);
    binaryLoad(arr,mid,right,arr2,++index);

}

int main(){
    int* nums;
    int index=0;

    int size = loadArray(nums,"random.txt");

    printArray(nums,size);
    bubbleSort(nums,size);
    printArray(nums,size);

    int* nums2 = new int[size];

    binaryLoad(nums,0,size-1,nums2,index);

    printArray(nums2,size);

    return 0;
}