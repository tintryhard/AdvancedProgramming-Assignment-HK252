public class Stock extends Instrument {
    private final double marketCap;
    private final String sector;

    public Stock(String symbol, String name, double currentPrice, double marketCap, String sector) {
        super(symbol, name, currentPrice);
        // TODO
        this.marketCap = marketCap;
        this.sector = sector;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public double riskScore() {
        // TODO
        if (marketCap < 1e9) {
            return 7.5;
        }
        else if (marketCap < 1e10) {
            return 5.0;
        }
        else return 3.0;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public String assetClass() {
        // TODO
        return "EQUITY";
        //throw new UnsupportedOperationException("TODO");
    }
    
    public double getMarketCap() {
        // TODO
        return this.marketCap;
        //throw new UnsupportedOperationException("TODO");
    }

    public String getSector() {
        // TODO
        return this.sector;
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public void accept(InstrumentVisitor visitor) {
        visitor.visit(this);
    }
}
