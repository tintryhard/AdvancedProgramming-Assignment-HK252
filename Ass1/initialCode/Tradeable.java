public interface Tradeable {
    String getSymbol();

    double getCurrentPriceValue();

    boolean isAvailableForTrading();

    default String getTradingInfo() {
        // TODO
        String status = isAvailableForTrading() ? "Available" : "Unavailable";
        return String.format("Tradeable: %s at $%.2f (%s)", this.getSymbol(), this.getCurrentPriceValue(), status);
        //throw new UnsupportedOperationException("TODO");
    }
}
