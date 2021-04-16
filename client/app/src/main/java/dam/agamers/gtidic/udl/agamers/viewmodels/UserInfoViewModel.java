package dam.agamers.gtidic.udl.agamers.viewmodels;

import androidx.lifecycle.MutableLiveData;

import dam.agamers.gtidic.udl.agamers.repositories.AccountRepo;

public class UserInfoViewModel {
    AccountRepo accountRepo = new AccountRepo();


    public void delete_account(){
        accountRepo.delete_account();
    }

    public MutableLiveData<Integer> getmResponseDeleteAccount(){
        return accountRepo.getmResponseDeleteAccount();
    }
}