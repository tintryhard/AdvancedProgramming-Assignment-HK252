public abstract class Derivative extends Instrument {

    public Derivative(String symbol, String name, double currentPrice) {
        super(symbol, name, currentPrice);
        // TODO
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public String assetClass() {
        // TODO
        return "DERIVATIVE";
        //throw new UnsupportedOperationException("TODO");
    }
}
