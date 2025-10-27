package reports;

public class W2WUATReport extends BaseReport {
    private int containers, storageRootUsed, storageRootAvail, storageDataUsed, storageDataAvail, externalFiles;
    private float ram;
    private boolean opensearch;

    @Override
    public void collectInputs() {
        System.out.print("Running containers (71): "); containers=sc.nextInt();
        System.out.print("Available storage '/': "); storageRootAvail=sc.nextInt();
        System.out.print("Used storage '/': "); storageRootUsed=sc.nextInt();
        System.out.print("Available storage 'data': "); storageDataAvail=sc.nextInt();
        System.out.print("Used storage 'data': "); storageDataUsed=sc.nextInt();
        System.out.print("RAM %: "); ram=sc.nextFloat();
        opensearch=askYesNo("Opensearch data available?");
        System.out.print("External files (17): "); externalFiles=sc.nextInt();
    }

    @Override
    public void generateReport() {
        System.out.println("\nW2W UAT Report ("+reportDate+")\n");
        System.out.println("1) Containers: "+containers+" => Total "+containers+((containers!=71)?".=> Issue":"."));
        System.out.println("2) Storage: "+storageRootAvail+"Gb/"+storageRootUsed+"% | "+storageDataAvail+"Gb/"+storageDataUsed+"% "+((storageRootUsed>75||storageDataUsed>75)?"=> Issue":""));
        System.out.println("3) All files downloaded in hsinteractive/hsbroadcast.");
        System.out.println("4) RAM "+ram+"% "+(ram>75?"=> Issue":""));
        System.out.println("5) Webclient/Hypertrade data fine.");
        System.out.println("6) Superadmin login works.");
        System.out.println("7) Brokeradmin login works.");
        System.out.println("8) External files: "+(externalFiles==17?"All 17 downloaded":"Only "+externalFiles+" downloaded"));
        System.out.println("9) Opensearch: "+(opensearch?"Available":"Not available => Issue"));
    }
}
