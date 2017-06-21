public class FindtheHat{
	public static void main(String []args){
		// Insertion Sort - O()

		System.out.println("Insertion Sort broken.");
		int b[] = {5,1,6,2,4,3};
		int i,j,temp;
		

		// Bubble Sort - O(n^2)
		System.out.println("Bubble Sort started.");
		int a[] = {5,1,6,2,4,3};

		for(i=0;i<6;i++){
			int flag = 0;
			for(j=0;j<6-i-1;j++){
				if(a[j]>a[j+1]){
					temp = a[j];
					a[j] = a[j+1];
					a[j+1] = temp;
					flag = 1;
				}
			}
			if(flag != 1){
				System.out.println("^ Solution found! ^");
				break;
			}
			// Print Array (after each sort step)
			for(int k=0; k<6; k++){
				System.out.print(a[k]);
			}
			System.out.println("");
		}
	}
}