package reports;

public class W2WProdReport extends BaseReport {
    private int ps, ns, dr, feedPsNs, feedDr;
    private int[] storageUsed=new int[10];
    private int[] storageAvail=new int[10];
    private float[] ram=new float[5];
    private boolean opensearch;
    private int[] feeders=new int[8];

    @Override
    public void collectInputs() {
        System.out.print("PS containers (59): "); ps=sc.nextInt();
        System.out.print("NS containers (55): "); ns=sc.nextInt();
        System.out.print("DR containers (55): "); dr=sc.nextInt();
        System.out.print("FEED PS/NS (28): "); feedPsNs=sc.nextInt();
        System.out.print("FEED DR (14): "); feedDr=sc.nextInt();

        String[] storageNames={"PS /","PS data","NS /","NS data","DR /","DR data","FEED PS/NS /","FEED PS/NS data","FEED DR /","FEED DR data"};
        for(int i=0;i<10;i++){
            System.out.print("Enter available storage for "+storageNames[i]+": ");
            storageAvail[i]=sc.nextInt();
            System.out.print("Enter used % for "+storageNames[i]+": ");
            storageUsed[i]=sc.nextInt();
        }

        String[] ramNames={"PS","NS","DR","FEED PS/NS","FEED DR"};
        for(int i=0;i<5;i++){
            System.out.print("Enter used RAM % in "+ramNames[i]+": ");
            ram[i]=sc.nextFloat();
        }

        opensearch=askYesNo("Opensearch data available?");
        String[] feederNames={"PS Kafka","PS Ignite","DR Kafka","DR Ignite","NS Kafka","NS Ignite"};
        for(int i=0;i<6;i++){
            System.out.print("Enter feeders connected in "+feederNames[i]+" (8): ");
            feeders[i]=sc.nextInt();
        }
    }

    @Override
    public void generateReport() {
        int total=ps+ns+dr+feedPsNs+feedDr;
        boolean cIssue=ps!=59||ns!=55||dr!=55||feedPsNs!=28||feedDr!=14;
        boolean sIssue=false,rIssue=false;
        for(int i:storageUsed) if(i>75){sIssue=true; break;}
        for(float f:ram) if(f>75){rIssue=true; break;}
        System.out.println("\nW2W PROD Report ("+reportDate+")\n");
        System.out.println("1) Containers: PS "+ps+" | NS "+ns+" | DR "+dr+" | FEED PS/NS "+feedPsNs+" | FEED DR "+feedDr+" => Total "+total+(cIssue?".=> Issue":"."));
        System.out.print("2) Storage: ");
        for(int i=0;i<10;i++) System.out.print(storageAvail[i]+"Gb/"+storageUsed[i]+"% | ");
        System.out.println((sIssue?"=> Issue":""));
        System.out.println("3) All files downloaded in PS | NS | DR | FEED PS/NS | FEED DR.");
        System.out.print("4) RAM: ");
        String[] ramNames={"PS","NS","DR","FEED PS/NS","FEED DR"};
        for(int i=0;i<5;i++) System.out.print(ramNames[i]+" "+ram[i]+"% | ");
        System.out.println((rIssue?"=> Issue":""));
        System.out.println("5) Webclient/Hypertrade data fine.");
        System.out.println("6) Superadmin login works.");
        System.out.println("7) Brokeradmin login works.");
        System.out.println("8) Opensearch: "+(opensearch?"Available":"Not available => Issue"));
        String[] feederNames={"PS Kafka","PS Ignite","DR Kafka","DR Ignite","NS Kafka","NS Ignite"};
        for(int i=0;i<6;i++) System.out.println((9+i)+") "+feederNames[i]+": "+(feeders[i]==8?"All connected":(feeders[i]>0?"Only "+feeders[i]+" connected => Issue":"None => Issue")));
    }
}
