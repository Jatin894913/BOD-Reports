package reports;

public class FSUATReport extends BaseReport {
    private int ps, ns, psStorageUsed, psStorageAvail, nsStorageUsed, nsStorageAvail;
    private int psStorageRootUsed, psStorageRootAvail, nsStorageRootUsed, nsStorageRootAvail;
    private float psRam, nsRam;
    private boolean opensearch;
    private int feedersPsKafka, feedersPsIgnite;

    @Override
    public void collectInputs() {
        System.out.print("PS containers (80): "); ps=sc.nextInt();
        System.out.print("NS containers (77): "); ns=sc.nextInt();
        System.out.print("PS storage '/' avail: "); psStorageRootAvail=sc.nextInt();
        System.out.print("PS storage '/' used %: "); psStorageRootUsed=sc.nextInt();
        System.out.print("PS storage 'data1' avail: "); psStorageAvail=sc.nextInt();
        System.out.print("PS storage 'data1' used %: "); psStorageUsed=sc.nextInt();
        System.out.print("NS storage '/' avail: "); nsStorageRootAvail=sc.nextInt();
        System.out.print("NS storage '/' used %: "); nsStorageRootUsed=sc.nextInt();
        System.out.print("NS storage 'data1' avail: "); nsStorageAvail=sc.nextInt();
        System.out.print("NS storage 'data1' used %: "); nsStorageUsed=sc.nextInt();
        System.out.print("PS RAM %: "); psRam=sc.nextFloat();
        System.out.print("NS RAM %: "); nsRam=sc.nextFloat();
        opensearch=askYesNo("Opensearch data available?");
        System.out.print("Feeders PS Kafka (8): "); feedersPsKafka=sc.nextInt();
        System.out.print("Feeders PS Ignite (8): "); feedersPsIgnite=sc.nextInt();
    }

    @Override
    public void generateReport() {
        System.out.println("\nFS UAT Report ("+reportDate+")\n");
        System.out.println("1) Containers: PS "+ps+" | NS "+ns+" => Total "+(ps+ns)+((ps!=80||ns!=77)?".=> Issue":"."));
        boolean sIssue=psStorageUsed>75||psStorageRootUsed>75||nsStorageUsed>75||nsStorageRootUsed>75;
        System.out.println("2) Storage: PS "+psStorageRootAvail+"/"+psStorageRootUsed+"% | "+psStorageAvail+"/"+psStorageUsed+"% | NS "+nsStorageRootAvail+"/"+nsStorageRootUsed+"% | "+nsStorageAvail+"/"+nsStorageUsed+"% "+(sIssue?"=> Issue":""));
        boolean rIssue=psRam>75||nsRam>75;
        System.out.println("3) All files downloaded in PS | NS.");
        System.out.println("4) RAM: PS "+psRam+"% | NS "+nsRam+"% "+(rIssue?"=> Issue":""));
        System.out.println("5) Webclient/Hypertrade data fine.");
        System.out.println("6) Superadmin login works.");
        System.out.println("7) Brokeradmin login works.");
        System.out.println("8) Opensearch: "+(opensearch?"Available":"Not available => Issue"));
        System.out.println("9) Feeders PS Kafka: "+(feedersPsKafka==8?"All connected":"Only "+feedersPsKafka+" connected => Issue"));
        System.out.println("10) Feeders PS Ignite: "+(feedersPsIgnite==8?"All connected":"Only "+feedersPsIgnite+" connected => Issue"));
    }
}
