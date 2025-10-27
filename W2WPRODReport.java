import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class W2WPRODReport {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        System.out.print("Enter running containers count in PS(expected 73): ");
        int psContainers = sc.nextInt();
        System.out.print("Enter running containers count in NS(expected 66): ");
        int nsContainers = sc.nextInt();
        System.out.print("Enter running containers count in DR(expected 66): ");
        int drContainers = sc.nextInt();
        boolean hasIssue = psContainers != 73 || nsContainers != 66 || drContainers != 66;

        sc.nextLine();

        System.out.print("Enter available storage in GB in PS '/': ");
        int storagePsrootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS '/': ");
        int storagePsrootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in PS 'data': ");
        int storagePsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS 'data': ");
        int storagePsUsed = sc.nextInt();

        System.out.print("Enter available storage in GB in NS '/': ");
        int storageNsrootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS '/': ");
        int storageNsrootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in NS 'data': ");
        int storageNsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS 'data': ");
        int storageNsUsed = sc.nextInt();

        System.out.print("Enter available storage in GB in DR '/': ");
        int storageDrrootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in DR '/': ");
        int storageDrrootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in DR 'data': ");
        int storageDrAvailable = sc.nextInt();
        System.out.print("Enter used storage % in DR 'data': ");
        int storageDrUsed = sc.nextInt();

        boolean hasStorageIssue =   storagePsrootUsed > 75 || storagePsUsed > 75 || 
                                    storageNsrootUsed > 75 || storageNsUsed > 75 || 
                                    storageDrrootUsed > 75 || storageDrUsed > 75; 

        sc.nextLine();

        System.out.print("Enter used RAM % in PS: ");
        float ramPs = sc.nextFloat();
        System.out.print("Enter used RAM % in NS: ");
        float ramNs = sc.nextFloat();
        System.out.print("Enter used RAM % in DR: ");
        float ramDr = sc.nextFloat();
        
        boolean hasRamIssue = ramPs > 75 || ramNs > 75 || ramDr > 75;

        sc.nextLine();

        System.out.println("Opensearch data is available or not: ");
        String Opensearchdata = sc.next();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in PS Kafka (expected 8): ");
        int feedersPsKafka = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in PS Ignite (expected 8): ");
        int feedersPsIgnite = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in DR Kafka (expected 8): ");
        int feedersDrKafka = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in DR Ignite (expected 8): ");
        int feedersDrIgnite = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in NS Kafka (expected 8): ");
        int feedersNsKafka = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in NS Ignite (expected 8): ");
        int feedersNsIgnite = sc.nextInt();

        sc.nextLine();

        sc.close();

        int totalContainers = psContainers + nsContainers + drContainers;

        System.out.println("\nW2W PROD Report (" + reportDate + "):\n");

        System.out.println("1) Running containers i.e., "
            + psContainers + " in PS | "
            + nsContainers + " in NS |"
            + drContainers + " in DR => Total " + totalContainers
            + (hasIssue ? ".=> Issue" : "."));

        System.out.println("2) Storage is available i.e., "
            + storagePsrootAvailable + "Gb available and Used is "
            + storagePsrootUsed + "% in '/' & "
            + storagePsAvailable + "Gb available and Used is "
            + storagePsUsed + "% in 'data' => PS|\n "

            + storageNsrootAvailable + "Gb available and used is "
            + storageNsrootUsed + "% in '/' & "
            + storageNsAvailable + "Gb available and used is "
            + storageNsUsed + "% in 'data'  => NS |\n "

            + storageDrrootAvailable + "Gb available and used is "
            + storageDrrootUsed + "% in '/' & "
            + storageDrAvailable + "Gb available and used is "
            + storageDrUsed + "% in 'data'  => DR |\n "
            
            + (hasStorageIssue ? "=> Issue" : ""));

        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast in PS | NS | DR | FEED PS/NS.");

        System.out.println("4) RAM is also available i.e., used RAM is "
            + ramPs + "% in PS | "
            + ramNs + "% in NS | "
            + ramDr + "% in DR |"
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

        if (feedersPsKafka == 8) {
            System.out.println("9) All 8 feeders are connected in PS Kafka.");
        } else if (0 < feedersPsKafka && feedersPsKafka < 8){
            System.out.println("9) Only " + feedersPsKafka + " feeders are connected in PS Kafka. => Issue");
        }
        else {
            System.out.println("9) No feeders are connected in PS Kafka. => Issue");
        }

        if (feedersPsIgnite == 8) {
            System.out.println("10) All 8 feeders are connected in PS Ignite.");
        } else if (0 < feedersPsIgnite && feedersPsIgnite < 8) {
            System.out.println("10) Only " + feedersPsIgnite + " feeders are connected in PS Ignite. => Issue");
        }
        else {
            System.out.println("10) No feeders are connected in PS Ignite. => Issue");
        }

        if (feedersDrKafka == 8){
            System.out.println("11) All 8 feeders are connected in DR Kafka");
        } else if (0 < feedersDrKafka && feedersDrKafka < 8) {
            System.out.println("11) Only " + feedersDrKafka + " feeders are connected in DR Kafka. => Issue");
        }
        else {
            System.out.println("11) No feeders are connected in DR Kafka. => Issue");
        }

        if (feedersDrIgnite == 8){
            System.out.println("12) All 8 feeders are connected in DR Ignite");
        } else if (0 < feedersDrIgnite && feedersDrIgnite < 8){
            System.out.println("12) Only " + feedersDrIgnite +" feeders are connected in DR Ignite. => Issue");
        }
        else {
            System.out.println("12) No feeders are connected in DR Ignite. => Issue");
        }

        if (feedersNsKafka == 8) {
            System.out.println("13) All 8 feeders are connected in NS Kafka.");
        } else if (0 < feedersNsKafka && feedersNsKafka < 8){
            System.out.println("13) Only " + feedersNsKafka + " feeders are connected in NS Kafka. => Issue");
        }
        else {
            System.out.println("13) No feeders are connected in NS Kafka. => Issue");
        }

        if (feedersNsIgnite == 8) {
            System.out.println("14 ) All 8 feeders are connected in NS Ignite.");
        } else if (0 < feedersNsIgnite && feedersNsIgnite < 8) {
            System.out.println("14) Only " + feedersNsIgnite + " feeders are connected in NS Ignite. => Issue");
        }
        else {
            System.out.println("14) No feeders are connected in NS Ignite. => Issue");
        }
    }
}
