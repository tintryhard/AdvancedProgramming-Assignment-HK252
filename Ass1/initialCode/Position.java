public class Position {
    private final Instrument instrument;
    private int quantity;
    private double averageCostBasis;

    public Position(Instrument instrument, int quantity, double averageCostBasis) {
        // TODO
        this.instrument = instrument;
        this.quantity = quantity;
        this.averageCostBasis = averageCostBasis;
        //throw new UnsupportedOperationException("TODO");
    }

    public double marketValue() {
        // TODO
        return this.quantity * instrument.getCurrentPriceValue();
        //throw new UnsupportedOperationException("TODO");
    }

    public double unrealizedPnL() {
        // TODO
        return this.marketValue() - this.quantity * this.averageCostBasis;
        //throw new UnsupportedOperationException("TODO");
    }

    public void addQuantity(int qty, double costBasis) {
        // TODO
        this.averageCostBasis = (this.quantity * this.averageCostBasis + qty * costBasis) / (this.quantity + qty);
        this.quantity += qty;
        //throw new UnsupportedOperationException("TODO");
    }

    public Instrument getInstrument() {
        // TODO
        return this.instrument;
        //throw new UnsupportedOperationException("TODO");
    }

    public int getQuantity() {
        // TODO
        return this.quantity;
        //throw new UnsupportedOperationException("TODO");
    }

    public double getAverageCostBasis() {
        // TODO
        return this.averageCostBasis;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public String toString() {
        // TODO
        return String.format("Position[symbol=%s, qty=%d, value=%.2f, pnl=%.2f]", instrument.getSymbol(), this.quantity, this.marketValue(), this.unrealizedPnL());
        //throw new UnsupportedOperationException("TODO");
    }
}
