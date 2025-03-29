package com.example.stockservice.service;

import com.example.stockservice.config.ApiKeyConfig;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.io.StringReader;
import java.lang.annotation.Documented;

@Service
@RequiredArgsConstructor
public class StockService {
    private final ApiKeyConfig apiKeyConfig;
    private final WebClient webClient;

    public void fetchStockData(){
        String API_URL = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="
                + apiKeyConfig.getApiKey() + "&numOfRows=1&pageNo=1";

        System.out.println(API_URL);

    }

}
