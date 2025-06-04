import java.util.Scanner;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class W2WUATReportGenerator {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Format today's date
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        // Collect required values only
        System.out.print("Enter total number of running containers: ");
        int containerCount = sc.nextInt();
        sc.nextLine(); // consume newline

        System.out.print("Enter available storage in '/' (GB): ");
        String storageRoot = sc.nextLine();

        System.out.print("Enter used storage in '/' (%): ");
        String storageRootUsed = sc.nextLine();

        System.out.print("Enter available storage in '/data' (GB): ");
        String storageData = sc.nextLine();

        System.out.print("Enter used storage in '/data' (%): ");
        String storageDataUsed = sc.nextLine();

        System.out.print("Enter used RAM percentage: ");
        String ramUsed = sc.nextLine();

        sc.close();

        // Print the report
        System.out.println("\nW2W UAT Report (" + reportDate + "): Before 9\n");

        System.out.println("1) All the required services i.e., " + containerCount + " containers are running.");
        System.out.println("2) All files are downloaded successfully in their respective location i.e, hsi & hsm.");
        System.out.println("3) Storage is also available i.e., " + storageRoot + " Gb available and Used is " + storageRootUsed +
                           "% in '/' and  " + storageData + " Gb available and Used is " + storageDataUsed + "% in '/data'.");
        System.out.println("4) RAM is also available i.e., used RAM is " + ramUsed + "%.");
        System.out.println("5) Data is coming in both webclient and hypertrade.");
        System.out.println("6) Getting otp in mobile and mail both, unable to add funds and able to purchase shares.");
        System.out.println("7) Yesterday's data is available in Opensearch.");
        System.out.println("8) Able to login in both brokeradmin and superadmin.");
    }
}
