package com.backend.stocks_backend.dao;
import org.springframework.data.jpa.repository.JpaRepository;
import com.backend.stocks_backend.model.Company;

public interface CompanyRepository extends JpaRepository<Company,Long> {
    // This interface will automatically inherit methods for CRUD operations
    // from JpaRepository, such as save, findById, findAll, deleteById, etc.
    // No additional code is needed here unless you want to define custom queries.
    Company findByCompanyCode(String companyCode);
    Company findByCompanyName(String companyName);

}
