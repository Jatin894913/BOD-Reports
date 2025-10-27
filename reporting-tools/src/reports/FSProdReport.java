package reports;

public class FSProdReport extends BaseReport {
    private int ps, ns, feedPs, feedNs, psStorageUsed, nsStorageUsed, feedPsStorageUsed, feedNsStorageUsed;
    private int psStorageAvail, nsStorageAvail, feedPsStorageAvail, feedNsStorageAvail;
    private float psRam, nsRam, feedPsRam, feedNsRam;
    private int externalFiles, feedersPs, feedersNs;
    private boolean opensearch;

    @Override
    public void collectInputs() {
        System.out.print("PS containers (61): "); ps=sc.nextInt();
        System.out.print("NS containers (58): "); ns=sc.nextInt();
        System.out.print("FEED PS (14): "); feedPs=sc.nextInt();
        System.out.print("FEED NS (13): "); feedNs=sc.nextInt();

        System.out.print("PS storage avail: "); psStorageAvail=sc.nextInt();
        System.out.print("PS storage used %: "); psStorageUsed=sc.nextInt();
        System.out.print("NS storage avail: "); nsStorageAvail=sc.nextInt();
        System.out.print("NS storage used %: "); nsStorageUsed=sc.nextInt();
        System.out.print("FEED PS storage avail: "); feedPsStorageAvail=sc.nextInt();
        System.out.print("FEED PS storage used %: "); feedPsStorageUsed=sc.nextInt();
        System.out.print("FEED NS storage avail: "); feedNsStorageAvail=sc.nextInt();
        System.out.print("FEED NS storage used %: "); feedNsStorageUsed=sc.nextInt();

        System.out.print("PS RAM %: "); psRam=sc.nextFloat();
        System.out.print("NS RAM %: "); nsRam=sc.nextFloat();
        System.out.print("FEED PS RAM %: "); feedPsRam=sc.nextFloat();
        System.out.print("FEED NS RAM %: "); feedNsRam=sc.nextFloat();

        System.out.print("External files count (17): "); externalFiles=sc.nextInt();
        opensearch=askYesNo("Opensearch data available?");
        System.out.print("Feeders PS (8): "); feedersPs=sc.nextInt();
        System.out.print("Feeders NS (8): "); feedersNs=sc.nextInt();
    }

    @Override
    public void generateReport() {
        int total=ps+ns+feedPs+feedNs;
        boolean cIssue=ps!=61||ns!=58||feedPs!=14||feedNs!=13;
        boolean sIssue=psStorageUsed>75||nsStorageUsed>75||feedPsStorageUsed>75||feedNsStorageUsed>75;
        boolean rIssue=psRam>75||nsRam>75||feedPsRam>75||feedNsRam>75;

        System.out.println("\nFS PROD Report ("+reportDate+")\n");
        System.out.println("1) Containers: PS "+ps+" | NS "+ns+" | FEED PS "+feedPs+" | FEED NS "+feedNs+" => Total "+total+(cIssue?".=> Issue":"."));
        System.out.println("2) Storage: PS "+psStorageAvail+"Gb/"+psStorageUsed+"% | NS "+nsStorageAvail+"Gb/"+nsStorageUsed+"% | FEED PS "+feedPsStorageAvail+"Gb/"+feedPsStorageUsed+"% | FEED NS "+feedNsStorageAvail+"Gb/"+feedNsStorageUsed+"% "+(sIssue?"=> Issue":""));
        System.out.println("3) All required files downloaded in PS | NS | FEED PS | FEED NS.");
        System.out.println("4) RAM: PS "+psRam+"% | NS "+nsRam+"% | FEED PS "+feedPsRam+"% | FEED NS "+feedNsRam+"% "+(rIssue?"=> Issue":""));
        System.out.println("5) Webclient and Hypertrade data fine.");
        System.out.println("6) Superadmin login works.");
        System.out.println("7) Brokeradmin login works.");
        System.out.println("8) External files: "+(externalFiles==17?"All 17 downloaded":"Only "+externalFiles+" downloaded"));
        System.out.println("9) Opensearch: "+(opensearch?"Available":"Not available => Issue"));
        System.out.println("10) Feeders PS: "+(feedersPs==8?"All connected":(feedersPs>0?"Only "+feedersPs+" connected => Issue":"None => Issue")));
        System.out.println("11) Feeders NS: "+(feedersNs==8?"All connected":(feedersNs>0?"Only "+feedersNs+" connected => Issue":"None => Issue")));
    }
}
