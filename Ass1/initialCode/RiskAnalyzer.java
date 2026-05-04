import java.util.*;

public class RiskAnalyzer<T extends Instrument> {
    private final List<T> instruments = new ArrayList<>();

    public void add(T instrument) {
        // TODO
        boolean isFound = false;
        for (T ins : instruments) {
            if (ins.getSymbol().equals(instrument.getSymbol())) {
                isFound = true;
                instruments.remove(ins);
                instruments.add(instrument);
                break;
            }
        }

        if (!isFound) {
            instruments.add(instrument);
        }
        //throw new UnsupportedOperationException("TODO");
    }

    public double averageRisk() {
        // TODO
        double sumRisk = 0.0;
        for (T ins : instruments) {
            sumRisk += ins.riskScore();
        }

        if (instruments.size() == 0) return 0.0;
        return sumRisk / instruments.size();
        //throw new UnsupportedOperationException("TODO");
    }

    public T highestRisk() {
        // TODO
        if (instruments.size() == 0) {
            throw new NoSuchElementException("No instruments.");
        }
        double maxRisk = instruments.get(0).riskScore();
        T maxCandidate = instruments.get(0);
        for (T ins : instruments) {
            double risk = ins.riskScore();
            if (risk > maxRisk) {
                maxRisk = risk;
                maxCandidate = ins;
            }
        }

        return maxCandidate;
        //throw new UnsupportedOperationException("TODO");
    }

    public T lowestRisk() {
        // TODO
        if (instruments.size() == 0) {
            throw new NoSuchElementException("No instruments.");
        }
        double minRisk = instruments.get(0).riskScore();
        T minCandidate = instruments.get(0);
        for (T ins : instruments) {
            double risk = ins.riskScore();
            if (risk < minRisk) {
                minRisk = risk;
                minCandidate = ins;
            }
        }

        return minCandidate;
        //throw new UnsupportedOperationException("TODO");
    }

    public List<T> getAboveRiskThreshold(double threshold) {
        // TODO
        List<T> candidates = new ArrayList<>();

        for (T ins : instruments) {
            if (ins.riskScore() > threshold) {
                candidates.add(ins);
            }
        }

        return candidates;
        //throw new UnsupportedOperationException("TODO");
    }
}
