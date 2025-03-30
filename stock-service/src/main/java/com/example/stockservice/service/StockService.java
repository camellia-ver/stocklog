package com.example.stockservice.service;

import com.example.stockservice.config.ApiKeyConfig;
import com.example.stockservice.model.StockDTO;
import lombok.RequiredArgsConstructor;
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
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class StockService {
    private final ApiKeyConfig apiKeyConfig;

    public void fetchStockData(int numOfRows, int pageNo){
        String apiUrl = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="
                + apiKeyConfig.getApiKey()
                + "&numOfRows=" + numOfRows
                + "&pageNo=" + pageNo;

        HttpURLConnection connection = null;

        try{
            URL url = new URL(apiUrl);
            connection = (HttpURLConnection)url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(10000);
            connection.setReadTimeout(10000);

            int responseCode = connection.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK){
                throw new IllegalStateException("API 요청 실패: " + responseCode);
            }

            try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))){
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null){
                    response.append(inputLine);
                }

                List<StockDTO> stockList = parseStockData(response.toString());
                stockList.forEach(System.out::println);
            }
        }catch (IOException e){
            throw new IllegalStateException(e.getMessage());
        }finally {
            if (connection != null){
                connection.disconnect();
            }
        }
    }

    private List<StockDTO> parseStockData(String xmlResponse){
        List<StockDTO> stockList = new ArrayList<>();

        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            InputSource is = new InputSource(new StringReader(xmlResponse));
            Document doc = builder.parse(is);

            NodeList itemList = doc.getElementsByTagName("item");
            for (int i = 0; i < itemList.getLength(); i++) {
                Node item = itemList.item(i);
                if (item.getNodeType() == Node.ELEMENT_NODE){
                    Element element = (Element) item;

                    StockDTO stock = StockDTO.builder()
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
                            .trqu(Integer.parseInt(getTextContent(element, "trqu")))
                            .trPrc(Integer.parseInt(getTextContent(element, "trPrc")))
                            .lstgStCnt(Integer.parseInt(getTextContent(element, "lstgStCnt")))
                            .mrktTotAmt(Integer.parseInt(getTextContent(element, "mrktTotAmt")))
                            .build();
                }
            }
        } catch (Exception e) {
            throw new IllegalStateException(e.getMessage());
        }

        return stockList;
    }

    private String getTextContent(Element element,String tagName){
        NodeList nodeList = element.getElementsByTagName(tagName);
        return (nodeList.getLength() > 0) ? nodeList.item(0).getTextContent() : "";
    }
}
