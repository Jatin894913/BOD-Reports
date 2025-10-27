import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class FSProdReport {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        System.out.print("Enter running containers count in PS(expected 61): ");
        int psContainers = sc.nextInt();
        System.out.print("Enter running containers count in NS(expected 58): ");
        int nsContainers = sc.nextInt();
        System.out.print("Enter running containers count in FEED PS(expected 14): ");
        int feedPsContainers = sc.nextInt();
        System.out.print("Enter running containers count in FEED NS(expected 13): ");
        int feedNsContainers = sc.nextInt();
        boolean hasIssue = psContainers != 61 || nsContainers != 58 || feedPsContainers != 14 || feedNsContainers != 13;

        sc.nextLine();

        System.out.print("Enter available storage in GB in PS 'data2': ");
        int storagePsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS 'data2': ");
        int storagePsUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in NS 'data2': ");
        int storageNsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS 'data2': ");
        int storageNsUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in FEED PS '/': ");
        int storageFeedPsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in FEED PS '/': ");
        int storageFeedPsUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in FEED NS '/': ");
        int storageFeedNsAvailable = sc.nextInt();
        System.out.print("Enter used storage % in FEED NS '/': ");
        int storageFeedNsUsed = sc.nextInt();
        boolean hasStorageIssue = storagePsUsed > 75 || storageNsUsed > 75 || storageFeedPsUsed > 75|| storageFeedNsUsed > 75;

        sc.nextLine();

        System.out.print("Enter used RAM % in PS: ");
        float ramPs = sc.nextFloat();
        System.out.print("Enter used RAM % in NS: ");
        float ramNs = sc.nextFloat();
        System.out.print("Enter used RAM % in FEED PS: ");
        float ramFeedPs = sc.nextFloat();
        System.out.print("Enter used RAM % in FEED NS: ");
        float ramFeedNs = sc.nextFloat();
        
        boolean hasRamIssue = ramPs > 75 || ramNs > 75 || ramFeedPs > 75 || ramFeedNs > 75;


        sc.nextLine();

        System.out.print("Enter number of external files downloaded (expected 17): ");
        int externalFilesCount = sc.nextInt();

        sc.nextLine();

        System.out.println("Opensearch data is available or not: ");
        String Opensearchdata = sc.next();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in PS (expected 8): ");
        int feedersPs = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in NS (expected 8): ");
        int feedersNs = sc.nextInt();

        sc.nextLine();

        sc.close();

        int totalContainers = psContainers + nsContainers + feedPsContainers + feedNsContainers;

        System.out.println("\nFS PROD Report (" + reportDate + "):\n");

        System.out.println("1) Running containers i.e., "
            + psContainers + " in PS | "
            + nsContainers + " in NS | FEED PS "
            + feedPsContainers + " | FEED NS "
            + feedNsContainers + " => Total " + totalContainers
            + (hasIssue ? ".=> Issue" : "."));

        System.out.println("2) Storage is also available i.e., "
            + storagePsAvailable + " Gb available and Used is "
            + storagePsUsed + "% in 'data2' => PS"
            + (storagePsUsed > 75 ? " => Issue" : "") + " | \n"
            
            + storageNsAvailable + " Gb available and used is "
            + storageNsUsed + "% in 'data2' => NS"
            + (storageNsUsed > 75 ? " => Issue" : "") + " | \n"

            + storageFeedPsAvailable + " Gb and Used is "
            + storageFeedPsUsed + "% in '/' => FEED PS"
            + (storageFeedPsUsed > 75 ? " => Issue" : "") + " | \n"
            
            + storageFeedNsAvailable + " Gb and used is "
            + storageFeedNsUsed + "% in '/' => FEED NS"
            + (storageFeedNsUsed > 75 ? " => Issue" : "") + ".");


        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast in PS | NS | FEED PS | FEED NS.");

        System.out.println("4) RAM is also available i.e., used RAM is "
            + ramPs + "% in PS | "
            + ramNs + "% in NS | "
            + ramFeedPs + "% in FEED PS | "
            + ramFeedNs + "% in FEED NS."
            + (hasRamIssue ? "=> Issue" : ""));

        System.out.println("5) Data is coming in both webclient and hypertrade. Able to login in hypertrade also chart is displaying proper data and no data is missing.");

        System.out.println("6) Able to login in superadmin and it is working properly.");

        System.out.println("7) The login page is working fine in brokeradmin.");

        if (externalFilesCount == 17) {
            System.out.println("8 ) All 17 external files are downloaded successfully.");
        } else {
            System.out.println("8 ) Only " + externalFilesCount + " external files are downloaded.");
        }

        if (Opensearchdata.equalsIgnoreCase("yes")){
            System.out.println("9) Yesterday's data is available in Opensearch.");
        }
        else{
            System.out.println("9) Yesterday's data is available in Opensearch. Data is available from . => Issue");
        }

        if (feedersPs == 8) {
            System.out.println("10) All 8 feeders are connected in PS.");
        } else if (0 < feedersPs && feedersPs < 8){
            System.out.println("10) Only " + feedersPs + " feeders are connected in PS. => Issue");
        }
        else {
            System.out.println("10) No feeders are connected in PS. => Issue");
        }

        if (feedersNs == 8) {
            System.out.println("11) All 8 feeders are connected in NS.");
        } else if (0 < feedersNs && feedersNs < 8){
            System.out.println("11) Only " + feedersNs + " feeders are connected in NS. => Issue");
        }
        else {
            System.out.println("11) No feeders are connected in NS. => Issue.");
        }
    }
}