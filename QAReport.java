import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class QAReport {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        String reportDate = LocalDate.now().format(formatter);

        System.out.print("Enter running containers count in QA(expected 73): ");
        int QAContainers = sc.nextInt();
        boolean hasIssue = QAContainers != 73;

        sc.nextLine();

        System.out.print("Enter available storage in GB in PS '/': ");
        int storageQArootAvailable = sc.nextInt();
        System.out.print("Enter used storage % in PS '/': ");
        int storageQArootUsed = sc.nextInt();
        System.out.print("Enter available storage in GB in NS 'Data': ");
        int storageQAAvailable = sc.nextInt();
        System.out.print("Enter used storage % in NS 'Data': ");
        int storageQAUsed = sc.nextInt();
        boolean hasStorageIssue = storageQArootUsed > 75 || storageQAUsed > 75;

        sc.nextLine();

        System.out.print("Enter used RAM % in PS: ");
        float ramQA = sc.nextFloat();        
        boolean hasRamIssue = ramQA > 75;


        sc.nextLine();

        System.out.print("Enter number of external files downloaded (expected 17): ");
        int externalFilesCount = sc.nextInt();

        sc.nextLine();

        System.out.println("Opensearch data is available or not: ");
        String Opensearchdata = sc.next();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in QA Kafka (expected 8): ");
        int feedersQAKafka = sc.nextInt();

        sc.nextLine();

        System.out.print("Enter number of feeders connected in QA Ignite (expected 8): ");
        int feedersQAIgnite = sc.nextInt();

        sc.nextLine();

        sc.close();

        int totalContainers = QAContainers;

        System.out.println("\nTTS QA Report (" + reportDate + "):\n");

        System.out.println("1) Running containers i.e., "
            + QAContainers + " in QA => Total " + totalContainers
            + (hasIssue ? ".=> Issue" : "."));

        System.out.println("2) Storage is also available i.e., "
            + storageQArootAvailable + " Gb available and Used is "
            + storageQArootUsed + "% in '/' & "
            + storageQAAvailable + " Gb available and used is "
            + storageQAUsed + "% in 'Data' "
            + (hasStorageIssue ? "=> Issue" : ""));

        System.out.println("3) All the required files are downloaded in both hsinteractive and hsbroadcast.");

        System.out.println("4) RAM is also available i.e., used RAM is "
            + ramQA + "% in QA | "
            + (hasRamIssue ? "=> Issue" : ""));

        System.out.println("5) Data is coming in both webclient and hypertrade. Able to login in hypertrade also chart is displaying proper data and no data is missing.");

        System.out.println("6) Able to login in superadmin and it is working properly.");

        System.out.println("7) The login page is working fine in brokeradmin.");

        if (externalFilesCount == 17) {
            System.out.println("8 ) All 17 external files are downloaded successfully.");
        } else {
            System.out.println("8) Only " + externalFilesCount + " external files are downloaded.");
        }

        if (Opensearchdata.equalsIgnoreCase("yes")){
            System.out.println("9) Yesterday's data is available in Opensearch.");
        }
        else{
            System.out.println("9) Yesterday's data is available in Opensearch. Data is available from . => Issue");
        }

        if (feedersQAKafka == 8) {
            System.out.println("10) All 8 feeders are connected in QA Kafka.");
        } else {
            System.out.println("10) Only " + feedersQAKafka + " feeders are connected in QA Kafka. => Issue");
        }

        if (feedersQAIgnite == 8) {
            System.out.println("11) All 8 feeders are connected in QA Ignite.");
        } else {
            System.out.println("11) Only " + feedersQAIgnite + " feeders are connected in QA Ignite. => Issue");
        }
    }
}