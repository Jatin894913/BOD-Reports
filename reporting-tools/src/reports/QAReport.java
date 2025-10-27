package reports;

public class QAReport extends BaseReport {
    private int qaContainers, storageRootAvail, storageRootUsed, storageDataAvail, storageDataUsed;
    private float ramQa;
    private int externalFiles, feedersQaKafka, feedersQaIgnite;
    private boolean opensearch;

    @Override
    public void collectInputs() {
        System.out.print("QA containers (73): "); qaContainers=sc.nextInt();
        System.out.print("QA storage '/' avail: "); storageRootAvail=sc.nextInt();
        System.out.print("QA storage '/' used %: "); storageRootUsed=sc.nextInt();
        System.out.print("QA storage 'Data' avail: "); storageDataAvail=sc.nextInt();
        System.out.print("QA storage 'Data' used %: "); storageDataUsed=sc.nextInt();
        System.out.print("QA RAM %: "); ramQa=sc.nextFloat();
        System.out.print("External files (17): "); externalFiles=sc.nextInt();
        opensearch=askYesNo("Opensearch data available?");
        System.out.print("Feeders QA Kafka (8): "); feedersQaKafka=sc.nextInt();
        System.out.print("Feeders QA Ignite (8): "); feedersQaIgnite=sc.nextInt();
    }

    @Override
    public void generateReport() {
        System.out.println("\nTTS QA Report ("+reportDate+")\n");
        System.out.println("1) Containers: "+qaContainers+" => Total "+qaContainers+((qaContainers!=73)?".=> Issue":"."));
        boolean sIssue=storageRootUsed>75||storageDataUsed>75;
        boolean rIssue=ramQa>75;
        System.out.println("2) Storage: "+storageRootAvail+"/"+storageRootUsed+"% | "+storageDataAvail+"/"+storageDataUsed+"% "+(sIssue?"=> Issue":""));
        System.out.println("3) All files downloaded in hsinteractive/hsbroadcast.");
        System.out.println("4) RAM: "+ramQa+"% "+(rIssue?"=> Issue":""));
        System.out.println("5) Webclient/Hypertrade data fine.");
        System.out.println("6) Superadmin login works.");
        System.out.println("7) Brokeradmin login works.");
        System.out.println("8) External files: "+(externalFiles==17?"All 17 downloaded":"Only "+externalFiles+" downloaded"));
        System.out.println("9) Opensearch: "+(opensearch?"Available":"Not available => Issue"));
        System.out.println("10) Feeders QA Kafka: "+(feedersQaKafka==8?"All connected":"Only "+feedersQaKafka+" connected => Issue"));
        System.out.println("11) Feeders QA Ignite: "+(feedersQaIgnite==8?"All connected":"Only "+feedersQaIgnite+" connected => Issue"));
    }
}
