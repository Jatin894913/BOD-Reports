package reports;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public abstract class BaseReport {
    protected static final Scanner sc = new Scanner(System.in);
    protected final String reportDate = LocalDate.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));
    public abstract void collectInputs();
    public abstract void generateReport();
    public void run() {
        collectInputs();
        generateReport();
    }
    protected boolean askYesNo(String msg) {
        System.out.print(msg + " (yes/no): ");
        return sc.next().equalsIgnoreCase("yes");
    }
}
