public class Future extends Derivative {
    private final double contractSize;
    private final int expiryDays;

    public Future(String symbol, String name, double currentPrice, double contractSize, int expiryDays) {
        super(symbol, name, currentPrice);
        // TODO
        this.contractSize = contractSize;
        this.expiryDays = expiryDays;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public double riskScore() {
        // TODO
        return 8.5;
        //throw new UnsupportedOperationException("TODO");
    }

    public double getContractSize() {
        // TODO
        return this.contractSize;
        //throw new UnsupportedOperationException("TODO");
    }

    public int getExpiryDays() {
        // TODO
        return this.expiryDays;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public void accept(InstrumentVisitor visitor) {
        visitor.visit(this);
    }
}
