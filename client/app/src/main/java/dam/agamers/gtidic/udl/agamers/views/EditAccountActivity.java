package dam.agamers.gtidic.udl.agamers.views;

import androidx.appcompat.app.AlertDialog;
import androidx.lifecycle.Observer;

import android.content.DialogInterface;
import android.database.DataSetObserver;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.SimpleAdapter;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;

import com.google.android.material.textfield.TextInputLayout;

import java.util.Arrays;

import dam.agamers.gtidic.udl.agamers.CommonActivity;
import dam.agamers.gtidic.udl.agamers.R;
import dam.agamers.gtidic.udl.agamers.models.Account;
import dam.agamers.gtidic.udl.agamers.models.enums.GenereEnum;
import dam.agamers.gtidic.udl.agamers.validators.AccountValidator;
import dam.agamers.gtidic.udl.agamers.viewmodels.EditAccountViewModel;

public class EditAccountActivity extends CommonActivity {

    private EditAccountViewModel editAccountViewModel;


    private TextInputLayout _username;
    private TextInputLayout _password;
    private TextInputLayout _short_description;
    private TextInputLayout _long_description;
    private TextInputLayout _email;
    private TextInputLayout _name;
    private TextInputLayout _surname;

    private boolean passwordValid = true; //TODO modificar quan es descarregui la informació
    private boolean short_descriptionValid = false;
    private boolean long_descriptionValid = false;
    private boolean emailValid = false;
    private boolean nameValid = false;
    private boolean surnameValid =false;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_account);
        getSupportActionBar().hide();

        editAccountViewModel = new EditAccountViewModel();


        _username = findViewById(R.id.edit_info_username);
        _password = findViewById(R.id.edit_info_password);
        _short_description = findViewById(R.id.edit_info_short_description);
        _long_description = findViewById(R.id.edit_info_long_description);
        _email = findViewById(R.id.edit_info_email);
        _name = findViewById(R.id.edit_info_first_name);
        _surname = findViewById(R.id.edit_info_surname);

        setInformation();
        init_validation();
        setSpinnerGenere();
    }

    private void setSpinnerGenere(){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle(R.string.genere_select_title);


        builder.setItems(Integer.parseInt((Arrays.toString(GenereEnum.values()))), new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        });


        AlertDialog alertDialog = builder.create();
        alertDialog.show();


    }



    private void setInformation(){
        editAccountViewModel.getAccountMutableLiveData().observe(this, new Observer<Account>() {
            @Override
            public void onChanged(Account account) {
                _username.getEditText().setText(account.getUsername());
                _username.setFocusable(false);
                _password.getEditText().setText(account.getPassword());
                _short_description.getEditText().setText(account.getShort_description());
                _long_description.getEditText().setText(account.getLong_description());
                _email.getEditText().setText(account.getEmail());
                _name.getEditText().setText(account.getName());
                _surname.getEditText().setText(account.getSurname());
                //TODO enxcara falten valors
            }
        });
    }

    private void init_validation(){

        _short_description.getEditText().addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                short_descriptionValid = s.toString().length() <= 100;
            }
        });

        _long_description.getEditText().addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                long_descriptionValid = s.toString().length() <= 2000;
            }
        });

        _email.getEditText().addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                emailValid = AccountValidator.check_mailValid(s.toString());
                updateForm(emailValid,_email,getString(R.string.error_mail_no_vàlid));
            }
        });

        _name.getEditText().addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                nameValid = AccountValidator.check_nameOrSurnameValid(s.toString());
                updateForm(nameValid,_name,getString(R.string.error_nom_no_vàlid));
            }
        });

        _surname.getEditText().addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                surnameValid = AccountValidator.check_nameOrSurnameValid(s.toString());
                updateForm(surnameValid,_surname,getString(R.string.error_cognom_no_vàlid));
            }
        });
    }

    //TODO JAVADOC
    private void updateForm(boolean isValid, TextInputLayout textInput, String error_msg) {
        if (!isValid) {
            textInput.setError(error_msg);
        } else {
            textInput.setErrorEnabled(false);
        }
        tots_camps_valids();
    }

    /**
     * Comprova que tots els camps del formaulari de registre són correctes, de ser així permetrà a l'usuari premer el botó de registre
     */
    private void tots_camps_valids(){
        Button b =findViewById(R.id.button_edit_info_save_exit);
        b.setEnabled(passwordValid && short_descriptionValid &&long_descriptionValid && emailValid && nameValid && surnameValid); //TODO mirar si la data es vàlida
    }


    public void save_and_exit(View view){
        Account account = new Account();

        //TODO falten verificacions

        account.setUsername(_username.getEditText().getText().toString());
        account.setPassword(_password.getEditText().getText().toString());
        account.setShort_description(_short_description.getEditText().getText().toString());
        account.setLong_description(_long_description.getEditText().getText().toString());
        account.setEmail(_email.getEditText().getText().toString());
        account.setName(_name.getEditText().getText().toString());
        account.setSurname(_surname.getEditText().getText().toString());



    }

    public void exit_no_save(View view){
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
        alertDialogBuilder.setTitle(R.string.edit_account_not_saved_title);
        alertDialogBuilder.setMessage(R.string.edit_account_message_data_not_saved);
        alertDialogBuilder.setNegativeButton(R.string.option_cancell, (dialog, which) -> {

        });
        alertDialogBuilder.setPositiveButton(R.string.option_ok, (dialog, which) -> goTo(UserInfoActivity.class));

        AlertDialog alertDialog = alertDialogBuilder.create();
        alertDialog.show();
    }

}