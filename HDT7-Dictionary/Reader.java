import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class Reader {

    /**
     * Metodo que lee un text file
     * @param fileName
     * @return
     */
    public static ArrayList<String> readFile(String fileName) {
        ArrayList<String> lines = new ArrayList<>();

        try {
            FileReader fileReader = new FileReader(fileName);

            BufferedReader bufferedReader = new BufferedReader(fileReader);

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line.getClass());
                lines.add(line);
            }

            bufferedReader.close();
        } catch (IOException ex) {
            System.out.println("Error al leer el archivo '" + fileName + "'");
            ex.printStackTrace();
        }
        return lines;
    }


    /**
     * Metodo que verifica si una linea tiene mas de una palabra
     */
    public static void checkMultipleWords (ArrayList <String> list) {
        for (String str : list) {
            String[] words = str.split(" ");
            if (words.length > 1) {
                System.out.println(str + " tiene más de una palabra.");
            } else {
                System.out.println(str + " tiene una sola palabra.");
            }
        }
    }





}
