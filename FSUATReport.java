import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class FSUATReport {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        System.out.print("Enter running containers count in PS(expected 80): ");
        int psContainers = sc.nextInt();
        System.out.print("Enter running containers count in NS(expected 77): ");
        int nsContainers = sc.nextInt();
        boolean hasIssue = psContainers != 80 || nsContainers != 77;

        sc.nextLine();

        System.out.print("Enter available storage in GB in PS '/': ");
        int storagePsrootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS '/': ");
        int storagePsrootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in PS 'data1': ");
        int storagePsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS 'data1': ");
        int storagePsUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in NS '/': ");
        int storageNsrootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS '/': ");
        int storageNsrootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in NS 'data1': ");
        int storageNsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS 'data1': ");
        int storageNsUsed = sc.nextInt();
        boolean hasStorageIssue = storagePsrootUsed > 75 || storagePsUsed > 75 || storageNsrootUsed > 75|| storageNsUsed > 75;

        sc.nextLine();

        System.out.print("Enter used RAM % in PS: ");
        float ramPs = sc.nextFloat();
        System.out.print("Enter used RAM % in NS: ");
        float ramNs = sc.nextFloat();
        
        boolean hasRamIssue = ramPs > 75 || ramNs > 75 ;

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

        sc.close();

        int totalContainers = psContainers + nsContainers ;

        System.out.println("\nFS UAT Report (" + reportDate + "):\n");

        System.out.println("1) Running containers i.e., "
            + psContainers + " in PS | "
            + nsContainers + " in NS => Total " + totalContainers
            + (hasIssue ? ".=> Issue" : "."));

        System.out.println("2) Storage is also available i.e., "
            + storagePsrootAvailable + " Gb available and Used is "
            + storagePsrootUsed + "% in '/' => PS| "
            + storagePsAvailable + " Gb available and used is "
            + storagePsUsed + "% in 'data1'  => PS | \n"

            + storageNsrootAvailable + " Gb and Used is "
            + storageNsrootUsed + "% in '/' => NS | "
            + storageNsAvailable + " Gb and used is "
            + storageNsUsed + "% in 'data1' => NS.\n"

            + (hasStorageIssue ? "=> Issue" : ""));

        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast in PS | NS.");

        System.out.println("4) RAM is also available i.e., used RAM is "
            + ramPs + "% in PS | "
            + ramNs + "% in NS "
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
        } else {
            System.out.println("9) Only " + feedersPsKafka + " feeders are connected in PS Kafka. => Issue");
        }

        if (feedersPsIgnite == 8) {
            System.out.println("10) All 8 feeders are connected in PS Ignite.");
        } else {
            System.out.println("10) Only " + feedersPsIgnite + " feeders are connected in PS Ignite. => Issue");
        }
    }
}