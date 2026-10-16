import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        
        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String response = "<!DOCTYPE html><html><head><title>Java Hello World</title></head>" +
                        "<body style='font-family: sans-serif; text-align: center; padding: 40px;'>" +
                        "<h1>Hello World from Java Application!</h1>" +
                        "<p>Student: <strong>Arnav Gupta</strong> (Roll: <strong>24bcs10063</strong>)</p>" +
                        "<p>Container Port: 8080</p></body></html>";
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            }
        });

        server.createContext("/health", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String response = "{\"status\":\"healthy\",\"service\":\"java-app\",\"student\":\"Arnav Gupta\"}";
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            }
        });

        server.setExecutor(null);
        System.out.println("Java HTTP Server started on port " + port);
        server.start();
    }
}
