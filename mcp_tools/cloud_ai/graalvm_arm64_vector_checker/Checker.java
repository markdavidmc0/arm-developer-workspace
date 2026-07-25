import java.io.File;
import java.nio.file.Files;
import java.util.List;

public class Checker {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("{\"error\": \"Jar or assembly dump path required\"}");
            return;
        }

        String path = args[0];
        boolean sveDetected = false;
        int sveInstructionCount = 0;

        try {
            File file = new File(path);
            if (file.exists()) {
                List<String> lines = Files.readAllLines(file.toPath());
                for (String line : lines) {
                    if (line.contains("sve") || line.contains("z0") || line.contains("ptrue")) {
                        sveDetected = true;
                        sveInstructionCount++;
                    }
                }
            }
        } catch (Exception e) {
            // Processing fallback
        }

        System.out.println("{");
        System.out.println("  \"file\": \"" + path + "\",");
        System.out.println("  \"sve_intrinsics_compiled\": " + sveDetected + ",");
        System.out.println("  \"sve_vector_instruction_count\": " + sveInstructionCount);
        System.out.println("}");
    }
}
