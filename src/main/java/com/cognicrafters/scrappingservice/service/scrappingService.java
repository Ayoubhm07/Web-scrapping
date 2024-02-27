package com.cognicrafters.scrappingservice.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class scrappingService {
    @Value("${python.script.path}")
    private String pythonServicePath;

    @Scheduled(cron = "0 0 0 * * MON")
    public void scrapeData() throws IOException, InterruptedException {
        ProcessBuilder processBuilder = new ProcessBuilder("python", pythonServicePath);
        Process process = processBuilder.start();
        process.waitFor();
        int exitCode = process.exitValue();
        if (exitCode != 0) {
            throw new RuntimeException("Le service a échoué avec le code de sortie " + exitCode);
        }
    }
}
