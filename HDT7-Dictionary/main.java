import java.util.ArrayList;

public class main {
    public static void main(String [] args){
        String path = "C:\\Users\\USUARIO\\OneDrive\\UVG\\Clases\\Tercer Semestre\\Estructura de datos\\Codes\\HDT7-Dictionary\\words.txt";

        ArrayList<String> arrayList;
        arrayList = Reader.readFile(path);

        Reader.checkMultipleWords(arrayList);








    }
}
