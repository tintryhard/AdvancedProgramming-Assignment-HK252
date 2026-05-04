public class TaxReportVisitor implements InstrumentVisitor {
    private double totalTaxLiability;
    private String report;

    public TaxReportVisitor() {
        this.totalTaxLiability = 0.0;
        report = "Tax[";
    }

    @Override
    public void visit(Stock stock) {
        double tax = 0.15 * stock.getCurrentPriceValue();
        this.totalTaxLiability += tax;
        report += String.format("%s=%.2f, ", stock.getSymbol(), tax);
    }

    @Override
    public void visit(Bond bond) {
        double tax = 0.3 * bond.annualCouponPayment(1);
        this.totalTaxLiability += tax;
        report += String.format("%s=%.2f, ", bond.getSymbol(), tax);
    }

    @Override
    public void visit(Option option) {
        double tax = 0.2 * option.getCurrentPriceValue();
        this.totalTaxLiability += tax;
        report += String.format("%s=%.2f, ", option.getSymbol(), tax);
    }

    @Override
    public void visit(Future future) {
        double tax = 0.2 * future.getCurrentPriceValue();
        this.totalTaxLiability += tax;
        report += String.format("%s=%.2f, ", future.getSymbol(), tax);
    }

    public double getTotalTaxLiability() {
        return this.totalTaxLiability;
    }

    public String getReport() {
        if (report.length() > 4) {
            return report.substring(0, report.length() - 2) + "]";
        }

        return report + "]";
    }
}

