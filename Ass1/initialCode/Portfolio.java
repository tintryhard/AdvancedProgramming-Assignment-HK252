import java.util.*;

public class Portfolio implements Observable<String> {
    private final String portfolioId;
    private final String ownerName;
    private final List<Position> positions;
    private final List<Observer<String>> observers;

    public Portfolio(String portfolioId, String ownerName) {
        // TODO
        this.portfolioId = portfolioId;
        this.ownerName = ownerName;
        this.positions = new ArrayList<>();
        this.observers = new ArrayList<>();
        //throw new UnsupportedOperationException("TODO");
    }

    public void addPosition(Instrument inst, int qty, double costBasis) {
        // TODO
        boolean isFound = false;
        for (Position p : this.positions) {
            if (p.getInstrument().getSymbol().equals(inst.getSymbol())) {
                isFound = true;
                p.addQuantity(qty, costBasis);
                break;
            }
        }

        if (!isFound) {
            Position newPos = new Position(inst, qty, costBasis);
            this.positions.add(newPos);
        }

        this.notifyObservers(String.format("ADDED: %s x%d", inst.getSymbol(), qty));
        //throw new UnsupportedOperationException("TODO");
    }

    public void removePosition(String symbol) throws PositionNotFoundException {
        // TODO
        boolean isFound = false;
        for (Position p : positions) {
            if (p.getInstrument().getSymbol().equals(symbol)) {
                isFound = true;
                positions.remove(p);
                break;
            }
        }

        if (!isFound) {
            throw new PositionNotFoundException("Position not found: " + symbol);
        }

        notifyObservers("REMOVED: " + symbol);
        //throw new UnsupportedOperationException("TODO");
    }

    public double totalMarketValue() {
        // TODO
        double sum = 0.0;
        for (Position p : positions) {
            sum += p.marketValue();
        }
        return sum;
        //throw new UnsupportedOperationException("TODO");
    }

    public double totalUnrealizedPnL() {
        // TODO
        double sum = 0.0;
        for (Position p : positions) {
            sum += p.unrealizedPnL();
        }
        return sum;
        //throw new UnsupportedOperationException("TODO");
    }

    public Position getPosition(String symbol) throws PositionNotFoundException {
        // TODO
        for (Position p : positions) {
            if (p.getInstrument().getSymbol().equals(symbol)) {
                return p;
            }
        }

        throw new PositionNotFoundException("Position not found: " + symbol);
        //throw new UnsupportedOperationException("TODO");
    }

    public List<Position> getPositionsSortedByValue() {
        // TODO
        List<Position> res = new ArrayList<>(positions);
        res.sort(Comparator.comparingDouble(Position::marketValue).reversed());

        return res;
        //throw new UnsupportedOperationException("TODO");
    }

    public Map<String, Double> allocationByAssetClass() {
        // TODO
        Map<String, Double> res = new HashMap<>();
        for (Position p : positions) {
            double value = p.marketValue();
            String assetName = p.getInstrument().assetClass();
            res.put(assetName, res.getOrDefault(assetName, 0.0) + value);
        }

        double totalValue = this.totalMarketValue();
        if (totalValue == 0) return res;

        for (Map.Entry<String, Double> entry : res.entrySet()) {
            double percentage = (entry.getValue() / totalValue) * 100;
            res.put(entry.getKey(), percentage);
        }

        return res;
        //throw new UnsupportedOperationException("TODO");
    }

    public void revalueAll(PricingStrategy strategy) {
        // TODO
        for (Position p : positions) {
            p.getInstrument().updatePrice(strategy.calculateFairValue(p.getInstrument()));
        }

        notifyObservers("REVALUED: " + strategy.strategyName());       
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public void addObserver(Observer<String> observer) {
        // TODO
        if (observer == null) return;
        if (observers.contains(observer)) {
            int idx = observers.indexOf(observer);
            observers.set(idx, observer);
        }
        else {
            observers.add(observer);
        }
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public void removeObserver(Observer<String> observer) {
        // TODO
        if (observer == null) return;

        observers.remove(observer);
        //throw new UnsupportedOperationException("TODO");
    }

    @Override
    public void notifyObservers(String event) {
        // TODO
        for (Observer<String> obs : observers) {
            obs.onEvent(event);
        }
        //throw new UnsupportedOperationException("TODO");
    }

    public String getPortfolioId() {
        // TODO
        return this.portfolioId;
        //throw new UnsupportedOperationException("TODO");
    }

    public String getOwnerName() {
        // TODO
        return this.ownerName;
        //throw new UnsupportedOperationException("TODO");
    }
}
