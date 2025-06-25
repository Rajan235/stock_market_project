package com.backend.stocks_backend.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.backend.stocks_backend.dao.CompanyRepository;
import com.backend.stocks_backend.model.Company;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CompanyService {
    private final CompanyRepository companyRepository;
    

    public List<Company>getAllCompanies() {
        return companyRepository.findAll();
    }
    public Company getCompanyById(Long companyId) {
        return companyRepository.findById(companyId)
                .orElseThrow(() -> new RuntimeException("Company not found with id: " + companyId));
    }

}
