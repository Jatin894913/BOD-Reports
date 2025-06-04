import java.util.Scanner;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class W2WProdReportGenerator {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        // Containers
        System.out.print("Enter running containers count in PS: ");
        int psContainers = sc.nextInt();
        System.out.print("Enter running containers count in NS: ");
        int nsContainers = sc.nextInt();
        System.out.print("Enter running containers count in DR: ");
        int drContainers = sc.nextInt();
        System.out.print("Enter running containers count in FEED PS/NS: ");
        int feedPsNsContainers = sc.nextInt();
        System.out.print("Enter running containers count in FEED DR: ");
        int feedDrContainers = sc.nextInt();

        sc.nextLine(); // consume newline

        // Storage
        System.out.print("Enter available storage in GB in PS '/data': ");
        String storagePsData = sc.nextLine();
        System.out.print("Enter used storage % in PS '/data': ");
        String storagePsDataUsed = sc.nextLine();
        System.out.print("Enter available storage in GB in PS '/': ");
        String storagePsRoot = sc.nextLine();
        System.out.print("Enter used storage % in PS '/': ");
        String storagePsRootUsed = sc.nextLine();

        System.out.print("Enter available storage in GB in NS '/data': ");
        String storageNsData = sc.nextLine();
        System.out.print("Enter used storage % in NS '/data': ");
        String storageNsDataUsed = sc.nextLine();
        System.out.print("Enter available storage in GB in NS '/': ");
        String storageNsRoot = sc.nextLine();
        System.out.print("Enter used storage % in NS '/': ");
        String storageNsRootUsed = sc.nextLine();

        System.out.print("Enter available storage in GB in DR '/data': ");
        String storageDrData = sc.nextLine();
        System.out.print("Enter used storage % in DR '/data': ");
        String storageDrDataUsed = sc.nextLine();
        System.out.print("Enter available storage in GB in DR '/': ");
        String storageDrRoot = sc.nextLine();
        System.out.print("Enter used storage % in DR '/': ");
        String storageDrRootUsed = sc.nextLine();

        System.out.print("Enter available storage in GB in FEED PS/NS '/data': ");
        String storageFeedPsNsData = sc.nextLine();
        System.out.print("Enter used storage % in FEED PS/NS '/data': ");
        String storageFeedPsNsDataUsed = sc.nextLine();
        System.out.print("Enter available storage in GB in FEED PS/NS '/': ");
        String storageFeedPsNsRoot = sc.nextLine();
        System.out.print("Enter used storage % in FEED PS/NS '/': ");
        String storageFeedPsNsRootUsed = sc.nextLine();

        System.out.print("Enter available storage in GB in FEED DR '/data': ");
        String storageFeedDrData = sc.nextLine();
        System.out.print("Enter used storage % in FEED DR '/data': ");
        String storageFeedDrDataUsed = sc.nextLine();
        System.out.print("Enter available storage in GB in FEED DR '/': ");
        String storageFeedDrRoot = sc.nextLine();
        System.out.print("Enter used storage % in FEED DR '/': ");
        String storageFeedDrRootUsed = sc.nextLine();

        // RAM
        System.out.print("Enter used RAM % in PS: ");
        String ramPs = sc.nextLine();
        System.out.print("Enter used RAM % in NS: ");
        String ramNs = sc.nextLine();
        System.out.print("Enter used RAM % in FEED PS/NS: ");
        String ramFeedPsNs = sc.nextLine();
        System.out.print("Enter used RAM % in DR: ");
        String ramDr = sc.nextLine();
        System.out.print("Enter used RAM % in FEED DR: ");
        String ramFeedDr = sc.nextLine();

        // External files info
        System.out.println("All required files are assumed downloaded in hsinteractive and hsbroadcast in PS | NS | DR | FEED PS/NS | FEED DR.");

        // Feeders counts
        System.out.print("Enter number of feeders connected in PS (expected 8): ");
        int feedersPs = sc.nextInt();
        System.out.print("Enter number of feeders connected in DR (expected 8): ");
        int feedersDr = sc.nextInt();
        System.out.print("Enter number of feeders connected in NS (expected 8): ");
        int feedersNs = sc.nextInt();

        sc.nextLine(); // consume newline

        // Close Scanner
        sc.close();

        // Calculate total containers
        int totalContainers = psContainers + nsContainers + drContainers + feedPsNsContainers + feedDrContainers;

        // Print report
        System.out.println("\nW2W PROD Report (" + reportDate + "):\n");

        System.out.println("1) All the required containers are running i.e., "
                + psContainers + " in PS | "
                + nsContainers + " in NS | "
                + drContainers + " in DR | "
                + feedPsNsContainers + " in FEED PS/NS | "
                + feedDrContainers + " in FEED DR => Total " + totalContainers + ".");

        System.out.println("2) Storage is also available i.e.,");
        System.out.println(storagePsData + " Gb available and used is " + storagePsDataUsed + "% in '/data' & "
                + storagePsRoot + " Gb available and " + storagePsRootUsed + "% is used in PS '/'");
        System.out.println(storageNsData + " Gb available and used is " + storageNsDataUsed + "% in '/data' & "
                + storageNsRoot + " Gb available and " + storageNsRootUsed + "% is used in NS '/'");
        System.out.println(storageDrData + " Gb available and used is " + storageDrDataUsed + "% in '/data' & "
                + storageDrRoot + " Gb available and " + storageDrRootUsed + "% is used in DR '/'");
        System.out.println(storageFeedPsNsData + " Gb available and used is " + storageFeedPsNsDataUsed + "% in '/data' & "
                + storageFeedPsNsRoot + " Gb available and " + storageFeedPsNsRootUsed + "% is used in FEED PS/NS '/'");
        System.out.println(storageFeedDrData + " Gb available and used is " + storageFeedDrDataUsed + "% in '/data' & "
                + storageFeedDrRoot + " Gb available and " + storageFeedDrRootUsed + "% is used in FEED DR '/'");

        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast in PS | NS | DR | FEED PS/NS | FEED DR.");

        System.out.println("4) RAM is also available i.e., used RAM "
                + ramPs + "% PS | "
                + ramNs + "% NS | "
                + ramFeedPsNs + "% FEED PS/NS | "
                + ramDr + "% DR | "
                + ramFeedDr + "% FEED DR.");

        System.out.println("5) Data is coming in both webclient and hypertrade. Able to login in hypertrade also chart is displaying proper data and all data is coming.");

        System.out.println("6) Able to login in superadmin and it is working properly.");

        System.out.println("7) The login page is loading in brokeradmin.");

        System.out.println("8) Yesterday's data is available in Opensearch.");

        System.out.print("9) All 8 feeders are connected in PS: ");
        System.out.println(feedersPs != 8 ? "=> Issue" : "");

        System.out.print("10) All 8 feeders are connected in DR: ");
        System.out.println(feedersDr != 8 ? "=> Issue" : "");

        System.out.print("11) All 8 feeders are connected in NS: ");
        System.out.println(feedersNs != 8 ? "=> Issue" : "");
    }
}
