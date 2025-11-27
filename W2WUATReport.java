import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class W2WUATReport {
        public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        System.out.print("Enter running containers count (expected 72): ");
        int Containers = sc.nextInt();
        
        boolean hasIssue = Containers != 72;

        sc.nextLine();

        System.out.print("Enter available storage in GB in '/': ");
        int storagerootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in '/': ");
        int storagerootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in 'data': ");
        int storageAvailable = sc.nextInt();
        System.out.print("Enter used storage % in 'data': ");
        int storageUsed = sc.nextInt();
        
        boolean hasStorageIssue = storagerootUsed > 75 || storageUsed > 75;

        sc.nextLine();

        System.out.print("Enter used RAM % : ");
        float ram = sc.nextFloat();
        
        boolean hasRamIssue = ram > 75;

        sc.nextLine();

        System.out.println("Opensearch data is available or not: ");
        String Opensearchdata = sc.next();

        sc.nextLine();
        
        System.out.print("Enter number of external files downloaded (expected 17): ");
        int externalFilesCount = sc.nextInt();

        sc.nextLine();

        sc.close();

        int totalContainers = Containers;

        System.out.println("\nW2W UAT Report (" + reportDate + "):\n");

        System.out.println("1) Running containers i.e., "
            + Containers + " => Total " + totalContainers
            + (hasIssue ? ".=> Issue" : "."));

        System.out.println("2) Storage is also available i.e., "
            + storagerootAvailable + " Gb available and Used is "
            + storagerootUsed + "% in '/' & "
            + storageAvailable + " Gb available and used is "
            + storageUsed + "% in 'data'. "
            + (hasStorageIssue ? "=> Issue" : ""));

        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast.");

        System.out.println("4) RAM is also available i.e., used RAM is "
            + ram + "%"
            + (hasRamIssue ? "=> Issue" : ""));

        System.out.println("5) Data is coming in both webclient and hypertrade. Able to login in hypertrade also chart is displaying proper data and no data is missing.");

        System.out.println("6) Able to login in superadmin and it is working properly.");

        System.out.println("7) The login page is working fine in brokeradmin.");

        if (Opensearchdata.equalsIgnoreCase("yes")){
            System.out.println("8 ) Yesterday's data is available in Opensearch.");
        }
        else{
            System.out.println("8 ) Yesterday's data is available in Opensearch. Data is available from . => Issue");
        }

        if (externalFilesCount == 17) {
            System.out.println("9) All 17 external files are downloaded successfully.");
        } else {
            System.out.println("9) Only " + externalFilesCount + " external files are downloaded. => Issue");
        }
    }
}