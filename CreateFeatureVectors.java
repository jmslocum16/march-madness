import java.io.*;
import java.util.*;

public class CreateFeatureVectors {
    // dump table format
   // G	MP	FG	FGA	FG%	2P	2PA	2P%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS	PTS/G


    static String[] mainHeaders = new String[] {"School", "Conf", "IsP5", "W", "L", "W/L%", "Seed"};
    static String[] tableStatsHeaders = new String[] {"FG%", "2P%", "3P%", "FT%", "FGA/G", "3PA/G", "FTA/G", "ORB/G", "DRB/G", "TRB/G", "AST/G", "STL/G", "BLK/G", "TOV/G", "PF/G", "PTS/G",
                                                     "2PTA%", "3PTA%", "ORB%", "SHOTS/G", "AST/TO%"};
    static String[] tableRankHeaders = new String[] {"FG", "FGA", "FG%", "2P", "2PA", "2P%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "PTS/G"};

    static String[] extraHeaders = new String[] {"SRS", "SRS Rank", "SOS", "SOS Rank", "ORtg", "ORtg Rank", "DRtg", "DRtg Rank", "Height (in.)", "Years Exp"};
    public static void main(String[] args) throws Exception {
        Scanner mainIn = new Scanner(new File(args[0]));
        Scanner dumpIn = new Scanner(new File(args[1]));
        int totalTeams = Integer.parseInt(args[2]);
        // print headers
        for (int i = 0; i < mainHeaders.length; i++) {
            if (i != 0) System.out.print("\t");
            System.out.print(mainHeaders[i]);
        }
        for (int i = 0; i < tableStatsHeaders.length; i++) {
            System.out.print("\t");
            System.out.print(tableStatsHeaders[i]);
        }
        for (int i = 0; i < tableRankHeaders.length; i++) {
            System.out.print("\t");
            System.out.print(tableRankHeaders[i] + " Rank");
        }
        for (int i = 0; i < tableStatsHeaders.length; i++) {
            System.out.print("\t");
            System.out.print("OPP " + tableStatsHeaders[i]);
        }
        for (int i = 0; i < tableRankHeaders.length; i++) {
            System.out.print("\t");
            System.out.print("OPP " + tableRankHeaders[i] + " Rank");
        }
        for (int i = 0; i < tableStatsHeaders.length; i++) {
            System.out.print("\t");
            System.out.print("DIFF " + tableStatsHeaders[i]);
        }
        for (int i = 0; i < tableRankHeaders.length; i++) {
            System.out.print("\t");
            System.out.print("DIFF " + tableRankHeaders[i] + " Rank");
        }

        for (int i = 0; i < extraHeaders.length; i++) {
            System.out.print("\t");
            System.out.print(extraHeaders[i]);
        }
        System.out.println();


        while (mainIn.hasNextLine()) {
            parseMain(mainIn);
            parseDump(dumpIn, totalTeams);
            System.out.println();
        }
    }

    static void parseMain(Scanner in) throws Exception {
        String[] tokens = in.nextLine().split("\t");
        System.out.print(tokens[0] + "\t" + tokens[1] + "\t");
        if (tokens[1].equals("Big 12") || tokens[1].equals("Big Ten") || tokens[1].equals("ACC") || tokens[1].equals("Pac-12") || tokens[1].equals("SEC")) {
            System.out.print("1");
        } else {
            System.out.print("0");
        }
        String[] WLTokens = tokens[2].split("-");
        System.out.print("\t" + WLTokens[0] + "\t" + WLTokens[1] + "\t");
        int wins = Integer.parseInt(WLTokens[0]);
        int losses = Integer.parseInt(WLTokens[1]);
        double WLPct = (1.0 * wins) / (wins + losses);
        System.out.printf("%.3f\t%s", WLPct, tokens[3]);
    }

    static void parseDump(Scanner in, int teams) throws Exception {
        in.nextLine();
        List<Double> myStats = parseDumpStats(in.nextLine());
        for (Double d : myStats) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        List<Double> myRanks = parseDumpRank(in.nextLine(), teams);
        for (Double d : myRanks) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        List<Double> theirStats = parseDumpStats(in.nextLine());
        for (Double d : theirStats) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        List<Double> theirRanks = parseDumpRank(in.nextLine(), teams);
        for (Double d : theirRanks) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        List<Double> statsDiff = diff(myStats, theirStats);
        for (Double d : statsDiff) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        List<Double> ranksDiff = diff(myRanks, theirRanks);
        for (Double d : ranksDiff) {
            System.out.print("\t");
            System.out.printf("%.3f", d);
        }
        // extra
        parseExtra(in.nextLine(), teams);
        parseExtra(in.nextLine(), teams);
        parseExtra(in.nextLine(), teams);
        parseExtra(in.nextLine(), teams);
        String[] height = parseExtra2(in.nextLine()).split("-");
        System.out.print("\t" + ((Integer.parseInt(height[0]) * 12) + Integer.parseInt(height[1])));
        System.out.print("\t" + parseExtra2(in.nextLine()));
        in.nextLine();
    }

    static void parseExtra(String line, int teams) {
        line = line.trim();
        int firstSpace = line.indexOf(" ");
        int secondSpace = line.indexOf(" ", firstSpace + 1);
        int thirdSpace = line.indexOf(" ", secondSpace + 1);
        String stat = line.substring(firstSpace + 1, secondSpace);
        int rank = Integer.parseInt(line.substring(secondSpace + 2, thirdSpace - 2));
        System.out.printf("\t%s\t%.3f", stat, (1.0 * rank) / teams);
    }

    static String parseExtra2(String line) {
        line = line.trim();
        int lastSpace = line.lastIndexOf(" ");
        return line.substring(lastSpace + 1);
    }

   // G	MP	FG	FGA	FG%	2P	2PA	2P%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS	PTS/G

   // static String[] tableStatsHeaders = new String[] {"FG%", "2P%", "3P%", "FT%", "FGA/G", "3PA/G", "FTA/G", "ORB/G", "DRB/G", "TRB/G", "AST/G", "STL/G", "BLK/G", "TOV/G", "PF/G", "PTS/G",
   //                                                "2PTA%", "3PTA%", "ORB%", "SHOTS/G", "AST/TO%"};


    public static List<Double> parseDumpStats(String line) throws Exception {
         System.err.println(line.substring(0, 10));
        List<Double> ret = new ArrayList<>();
        Scanner in = new Scanner(line).useDelimiter("\t");
        in.next();
        int games = in.nextInt();
        int minutes = in.nextInt();
        int fg = in.nextInt();
        int fga = in.nextInt();
        double fgPct = in.nextDouble();
        ret.add(fgPct);
        int fg2 = in.nextInt();
        int fg2a = in.nextInt();
        double fg2pct = in.nextDouble();
        ret.add(fg2pct);
        int fg3 = in.nextInt();
        int fg3a = in.nextInt();
        double fg3Pct = in.nextDouble();
        ret.add(fgPct);
        int ft = in.nextInt();
        int fta = in.nextInt();
        double ftPct = in.nextDouble();
        ret.add(ftPct);
        ret.add((1.0 * fga) / games);
        ret.add((1.0 * fg3a) / games);
        ret.add((1.0 * fta) / games);
        int orb = in.nextInt();
        ret.add((1.0 * orb) / games);
        int drb = in.nextInt();
        ret.add((1.0 * drb) / games);
        int trb = in.nextInt();
        ret.add((1.0 * trb) / games);
        int ast = in.nextInt();
        ret.add((1.0 * ast) / games);
        int stl = in.nextInt();
        ret.add((1.0 * stl) / games);
        int blk = in.nextInt();
        ret.add((1.0 * blk) / games);
        int tov = in.nextInt();
        ret.add((1.0 * tov) / games);
        int pf = in.nextInt();
        ret.add((1.0 * pf) / games);
        in.next();
        double ppg = in.nextDouble();
        ret.add(ppg);
        ret.add((1.0 * fg2a) / fga);
        ret.add((1.0 * fg3a) / fga);
        ret.add((1.0 * orb) / trb);
        ret.add((1.0 * fga) / games);
        ret.add((1.0 * ast) / tov);
        return ret;
   //                                                "2PTA%", "3PTA%", "ORB%", "SHOTS/G", "AST/TO%"};
    }

// G	MP	FG	FGA	FG%	2P	2PA	2P%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS	PTS/G

    // static String[] tableRankHeaders = new String[] {"FG", "FGA", "FG%", "2P", "2PA", "2P%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "PTS/G"};
    public static List<Double> parseDumpRank(String line, int teams) {
        List<Double> ret = new ArrayList<>();

        String[] tokens = line.split("\\s+");
        for (int i = 1; i < tokens.length; i++) {
            String t = tokens[i];
            int rank = Integer.parseInt(t.substring(0, t.length() - 2));
            ret.add((1.0 * rank) / teams);
        }
        return ret;
    }

    public static List<Double> diff(List<Double> my, List<Double> theirs) {
        if (my.size() != theirs.size()) throw new IllegalStateException();
        List<Double> ret = new ArrayList<>();
        for (int i = 0; i < my.size(); i++) {
            ret.add(my.get(i) - theirs.get(i));
        }
        return ret;
    }
}

