package launcher;

import java.util.Scanner;
import reports.*;

public class ReportLauncher {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        boolean cont=true;
        while(cont){
            System.out.println("\n=== Report Launcher ===");
            System.out.println("1. FS PROD | 2. W2W PROD | 3. W2W UAT | 4. FS UAT | 5. QA | 0. Exit");
            System.out.print("Choose report: ");
            int choice=sc.nextInt();
            BaseReport r=null;
            switch(choice){
                case 1: r=new FSProdReport(); break;
                case 2: r=new W2WProdReport(); break;
                case 3: r=new W2WUATReport(); break;
                case 4: r=new FSUATReport(); break;
                case 5: r=new QAReport(); break;
                case 0: cont=false; continue;
                default: System.out.println("Invalid choice"); continue;
            }
            if(r!=null) r.run();
            System.out.print("\nRun another report? (yes/no): ");
            cont=sc.next().equalsIgnoreCase("yes");
        }
        System.out.println("Exiting Report Launcher.");
        sc.close();
    }
}
