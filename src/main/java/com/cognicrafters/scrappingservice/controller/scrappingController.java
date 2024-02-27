package com.cognicrafters.scrappingservice.controller;

import com.cognicrafters.scrappingservice.service.scrappingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class scrappingController {

    private final scrappingService scrappingservice;

    @Autowired
    public scrappingController(scrappingService scrappingservice) {
        this.scrappingservice = scrappingservice;
    }

    @GetMapping("/scrape")
    public String scrape() {
        try {
            scrappingservice.scrapeData();
            return "Scraping réussi.";
        } catch (Exception e) {
            e.printStackTrace();
            return "Erreur lors du scraping.";
        }
    }
}
