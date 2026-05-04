public class Option extends Derivative {
    private final double strikePrice;
    private final boolean isCall;
    private final int expiryDays;

    public Option(String symbol, String name, double currentPrice, double strikePrice, boolean isCall, int expiryDays) {
        super(symbol, name, currentPrice);
        // TODO
        this.strikePrice = strikePrice;
        this.isCall = isCall;
        this.expiryDays = expiryDays;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public double riskScore() {
        // TODO
        return 8.5;
        //throw new UnsupportedOperationException("TODO");
    }
    
    public boolean isInTheMoney(double spotPrice) {
        // TODO
        if (this.isCall) {
            return spotPrice > this.strikePrice;
        }
        else return spotPrice < this.strikePrice;
        //throw new UnsupportedOperationException("TODO");
    }

    public double getStrikePrice() {
        // TODO
        return this.strikePrice;
        //throw new UnsupportedOperationException("TODO");
    }

    public boolean isCall() {
        // TODO
        return this.isCall;
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
