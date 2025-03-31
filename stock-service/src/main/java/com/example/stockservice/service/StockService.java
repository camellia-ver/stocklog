package com.example.stockservice.service;

import com.example.stockservice.config.ApiKeyConfig;
import com.example.stockservice.domain.Stock;
import com.example.stockservice.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
@RequiredArgsConstructor
public class StockService {
    private final ApiKeyConfig apiKeyConfig;
    private final StockRepository stockRepository;

    @Scheduled(cron = "0 0 8 * * MON-FRI")
    public void fetchStockData(){
        int numOfRows = 9999;
        int pageNo = 1;

        LocalDate today = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");
        String formattedDate = today.format(formatter);

        String apiUrl = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="
                + apiKeyConfig.getKey()
                + "&numOfRows=" + numOfRows
                + "&pageNo=" + pageNo
                + "&basDt=" + formattedDate;
        HttpURLConnection connection = null;

        try{
            URI uri = URI.create(apiUrl);
            URL url = uri.toURL();
            connection = (HttpURLConnection)url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(10000);
            connection.setReadTimeout(10000);

            int responseCode = connection.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK){
                throw new IllegalStateException("API 요청 실패: " + responseCode);
            }

            try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))){
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null){
                    response.append(inputLine);
                }

                parseStockData(response.toString());
            }
        }catch (IOException e){
            throw new IllegalStateException(e.getMessage());
        }finally {
            if (connection != null){
                connection.disconnect();
            }
        }
    }

    private void parseStockData(String xmlResponse){
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            InputSource is = new InputSource(new StringReader(xmlResponse));
            Document doc = builder.parse(is);

            NodeList itemList = doc.getElementsByTagName("item");
            List<Stock> stocks = new ArrayList<>();
            for (int i = 0; i < itemList.getLength(); i++) {
                Node item = itemList.item(i);

                if (item.getNodeType() == Node.ELEMENT_NODE){
                    Element element = (Element) item;

                    Stock stock = Stock.builder()
                            .srtnCd(getTextContent(element, "srtnCd"))
                            .isinCd(getTextContent(element, "isinCd"))
                            .itmsNm(getTextContent(element, "itmsNm"))
                            .mrktCtg(getTextContent(element, "mrktCtg"))
                            .clpr(Integer.parseInt(getTextContent(element, "clpr")))
                            .vs(Integer.parseInt(getTextContent(element, "vs")))
                            .fltRt(Double.parseDouble(getTextContent(element, "fltRt")))
                            .mkp(Integer.parseInt(getTextContent(element, "mkp")))
                            .hipr(Integer.parseInt(getTextContent(element, "hipr")))
                            .lopr(Integer.parseInt(getTextContent(element, "lopr")))
                            .trqu(Long.parseLong(getTextContent(element, "trqu")))
                            .trPrc(Long.parseLong(getTextContent(element, "trPrc")))
                            .lstgStCnt(Long.parseLong(getTextContent(element, "lstgStCnt")))
                            .mrktTotAmt(Double.parseDouble(getTextContent(element, "mrktTotAmt")))
                            .build();

                    stocks.add(stock);
                }
            }
            stockRepository.saveAll(stocks);
        } catch (Exception e) {
            throw new IllegalStateException(e.getMessage());
        }
    }

    private String getTextContent(Element element,String tagName){
        NodeList nodeList = element.getElementsByTagName(tagName);
        String content = (nodeList.getLength() > 0) ? nodeList.item(0).getTextContent() : null;
        return content != null ? content : "";
    }
}
