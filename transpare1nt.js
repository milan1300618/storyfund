const MAX_ROWS_TABLE = 25;
var transparentAccountsTableRows = [];
var transparentTransactionsTableRows = [];
var servicePageNumber = 0;
var tablePageNumber = 0;
var hasMoreRecords = true;
var accountNumberTransactions = "";

$(document).ready(function () {
    loadTransactionsFromIbanQueryParam();
    setDateFiltersDefaultValues();
    $.fn.addDatePicker();

    showAllAccountsOnClick();

    $('#searchAccounts').on('click', function () {
        hideErrorMessageAccounts();

        $('#showAllAccounts').css({"color": "#007A91", "text-decoration": "underline #00a0bf 1px"});
        showAllAccountsOnClick();

        var accountOwner = $('#accountOwnerInput').val();
        var iban = $("#ibanInput").val();
        if (!accountOwner && !iban) {
            $(".transparent-accounts .transparent-accounts-errors.no-input").show();
        } else if (isValidSearch(accountOwner, iban)) {
            tablePageNumber = 0;
            servicePageNumber = 0;
            getAccountsFromService(accountOwner, iban);
        } else {
            $(".transparent-accounts .transparent-accounts-errors.error-iban").show();
        }
    });

    $('.transparent-accounts .pages-navigator .accounts-previous-page').on('click', function () {
        //previous page
        tablePageNumber--;
        if (tablePageNumber === -1) {
            servicePageNumber -= 2;
        }
        displayAccountsTable();
    });

    $('.transparent-accounts .pages-navigator .accounts-next-page').on('click', function () {
        //next page
        tablePageNumber++;
        displayAccountsTable();
    });


    $('.transparent-transactions .transactions-back').on('click', function () {
        $('section.transparent-transactions').hide();
        $('section.transparent-accounts').show();
        hideErrorMessageTransactions();
        removeIBANQueryParam();
    });

    $('#searchTransactions').on('click', function () {
        clearTransactionsTable();
        hideErrorMessageTransactions();
        var transactionsInput = $('#transactionsInput').val();
        if (transactionsInput) {
            var {fromDate, toDate} = getFromToDates();

            servicePageNumber = 0;
            tablePageNumber = 0;
            getTransactionsFromService(fromDate, toDate, transactionsInput);
        } else {
            $('.transparent-transactions .pages-navigator .transaction-next-page').hide();
            $(".transparent-transactions .transparent-accounts-errors.transactions-no-input").show();
        }
    });

    $('.transparent-transactions .pages-navigator .transaction-previous-page').on('click', function () {
        //previous page
        tablePageNumber--;
        if (tablePageNumber === -1) {
            servicePageNumber -= 2;
        }
        displayTransactionsTable();
        $(".transparent-transactions .table-responsive table tbody tr[tabindex='0']").first().focus();
    });

    $('.transparent-transactions .pages-navigator .transaction-next-page').on('click', function () {
        //next page
        tablePageNumber++;
        displayTransactionsTable();
        $(".transparent-transactions .table-responsive table tbody tr[tabindex='0']").first().focus();
    });

});

function setDateFiltersDefaultValues(){
    var toDate = new Date();
    var fromDate = new Date();
    fromDate.setMonth(fromDate.getMonth() - 1);

    $('#datepicker-filter-chart-to').val(formatDateDayMonthYear(toDate));
    $('#datepicker-filter-chart-from').val(formatDateDayMonthYear(fromDate));
}

$.fn.addDatePicker = function (){
    $("body").on("click keyup", ".date.form-control", function(e) {
        e.stopImmediatePropagation();
        e.preventDefault();
        if(e.type === "click" || e.key === "Enter" || e.key === " ") {
            var isExpanded = $(this).attr('aria-expanded') === 'true';
            $(this).attr('aria-expanded', !isExpanded);
            resizeDatepicker($(this));
            positionDatepicker($(this));
            $(this).next().trigger("click");
        }

        var $datepickerTable = $(this).parents('.calendar-area').find('.datepicker-calendar table');
        if($datepickerTable.width() > 420) {
            $datepickerTable.find("th abbr").css("font-size", "12px");
        }
    });

    var language = $('html').attr('lang');

    if (language === undefined) {
        language = 'en';
    }

    var date = new Date();
    var currentDate = ('0' + date.getDate()).slice(-2) + "/" + ('0' + (date.getMonth() + 1)).slice(-2) + "/" + date.getFullYear();
    $("body").append('<script type="text/javascript" src="/etc/designs/cee2020-pws/clientLibs/datepicker-locales/js-source/' + language + '.js"></script>');

    $('#datepicker-filter-chart-from, #datepicker-filter-chart-to').datepicker({
        firstDayOfWeek: Date.dp_locales.firstday_of_week,
        daysOfWeekDisabled: [],
        inputFormat: ["dd/MM/yyyy"],
        outputFormat: 'dd/MM/yyyy',
        max: currentDate
    }).on("change", function () {
        $(this).attr('aria-expanded', 'false');
        var fromDateStr = $("#datepicker-filter-chart-from").val();
        var toDateStr = $("#datepicker-filter-chart-to").val();

        var fromParts = fromDateStr.split('/');
        var toParts = toDateStr.split('/');

        if (fromParts.length === 3 && toParts.length === 3) {
            var fromDate = new Date(fromParts[2], fromParts[1] - 1, fromParts[0]);
            var toDate = new Date(toParts[2], toParts[1] - 1, toParts[0]);

            if (fromDate > toDate) {
                var id = $(this).attr('id');
                if (id === 'datepicker-filter-chart-from') {
                    $("#datepicker-filter-chart-to").val(fromDateStr);
                } else {
                    $("#datepicker-filter-chart-from").val(toDateStr);
                }
            }
        }

        onChangeDateCallService();
    });

};

function resizeDatepicker($element) {
    var $datepicker= $element.parents('.calendar-area').find('.datepicker-calendar');
    //tooltip shift from container overflow
    var container = $element.parents(".container");
    var container_width = container.width() - 2; // minus border
    if(container_width < 422) {
        $datepicker.css("width", container_width);
    } else {
        $datepicker.css("width", "");
    }
}

function positionDatepicker($element) {
    var $datepicker= $element.parents('.calendar-area').find('.datepicker-calendar');
    var datepicker_width = $datepicker.outerWidth();
    var input_offset_left = $element.offset().left;

    //tooltip shift from container overflow
    var container = $element.parents(".container");
    var container_width = container.outerWidth() - parseInt(container.css('padding-right'));
    var cointainer_offset_left = container.offset().left;

    var position_shift = datepicker_width  + input_offset_left - container_width - cointainer_offset_left;

    if(position_shift > 0) {
        //tooltip arrow  position
        $datepicker.css({'left': (-1) * position_shift, 'top': '45px'});
    } else {
        $datepicker.css({'left': '', 'top': '35px'});
    }
}

function hideErrorMessageAccounts() {
    $('.transparent-accounts .table-accounts').hide();
    $(".transparent-accounts .transparent-accounts-errors.no-input").hide();
    $(".transparent-accounts .transparent-accounts-errors.error-iban").hide();
    $(".transparent-accounts .transparent-accounts-errors.no-results").hide();
}

function showAllAccountsOnClick() {
    $('#showAllAccounts').on('click', function (event) {
        event.preventDefault();
        hideErrorMessageAccounts();
        //clear inputs
        $('#accountOwnerInput').val("");
        $("#ibanInput").val("");

        $(this).css({"color": "#666666", "text-decoration": "underline #666666 1px"});

        tablePageNumber = 0;
        servicePageNumber = 0;
        getAccountsFromService();
        $(this).off('click');
    });
}

function isValidSearch(accountOwner, iban) {
    if (accountOwner && !iban) {
        return true;
    }
    if (iban && $('#ibanInput').is(':valid')) {
        return isValidIban(iban);
    }
    return false;
}

function isValidIban(iban) {
    if (entityCode === 'CZ' && iban.substr(0, 2) === 'CZ' && iban.substr(4, 4) === '2700') {
        return true;
    }
    if (entityCode === 'SK' && iban.substr(0, 2) === 'SK' && iban.substr(4, 4) === '1111') {
        return true;
    }
    return false;
}

function getAccountsFromService(accountOwner, iban) {
    var data = getInputDataAccounts(accountOwner, iban);
    $.ajax({
        type: 'GET',
        url: '/show.pws.transparentAccounts.html',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data: data,
        success: function (data) {
            if (data && data.iHubResponseInfo) {
                if (data.iHubResponseInfo.length > 0) {
                    transparentAccountsTableRows = data.iHubResponseInfo;
                    hasMoreRecords = data.hasMoreRecords;

                    displayAccountsTable();
                } else {
                    $(".transparent-accounts .transparent-accounts-errors.no-results").show();
                }
            } else {
                $(".transparent-accounts .transparent-accounts-errors.no-results").show();
            }
        },
        error: function () {
            $(".transparent-accounts .transparent-accounts-errors.no-results").show();
        }
    });
}

function getInputDataAccounts(accountOwner, iban) {
    var data = {};
    if (accountOwner) {
        data.accountOwner = encodeURIComponent(accountOwner);
    }

    if (iban) {
        data.iban = iban;
    }

    data.entityCode = $("#transparentAccountEntityCode").val();

    servicePageNumber++;
    if (servicePageNumber > 0) {
        data.pageNumber = servicePageNumber;
    } else {
        data.pageNumber = 1;
    }
    return data;
}

function displayAccountsTable() {
    //clear table
    var tableBody = $('.transparent-accounts .table-accounts .table-responsive tbody');
    tableBody.find("tr:gt(0)").remove();

    var getNewPageFromService = false;
    if(tablePageNumber === 4) {
        getNewPageFromService = true;
        tablePageNumber = 0;
    }
    if(tablePageNumber === -1) {
        getNewPageFromService = true;
        tablePageNumber = 3;
    }

    if (getNewPageFromService) {
        var accountOwner = $('#accountOwnerInput').val();
        var iban = $("#ibanInput").val();
        getAccountsFromService(accountOwner, iban);
        return;
    }

    var startIndex = tablePageNumber * MAX_ROWS_TABLE;
    while (startIndex < (tablePageNumber + 1) * MAX_ROWS_TABLE) {
        if (transparentAccountsTableRows[startIndex]) {
            var row = "<tr tabindex='0' data-balance='" + transparentAccountsTableRows[startIndex].balance + "' " +
                "data-accountnumber='" + transparentAccountsTableRows[startIndex].accountNumber + "' " +
                "data-currencycode='" + transparentAccountsTableRows[startIndex].currency + "'>" +
                    "<td>" + transparentAccountsTableRows[startIndex].accountOwner + "</td>" +
                    "<td>" + transparentAccountsTableRows[startIndex].accountIBAN + "</td>" +
            "</tr>";
            tableBody.append(row);
        }
        startIndex++;
    }

    var $previousPage = $('.transparent-accounts .pages-navigator .accounts-previous-page');
    var $nextPage = $('.transparent-accounts .pages-navigator .accounts-next-page');
    showHideTableButtons($previousPage, $nextPage, transparentAccountsTableRows.length);

    $('.transparent-accounts .table-accounts').show();

    onClickDisplayTransactionList();

}

function showHideTableButtons($previousPage, $nextPage, rowsLength) {
    if (tablePageNumber === 0 && servicePageNumber === 1) {
        $previousPage.hide();
    } else {
        $previousPage.show();
    }

    var numberOfPages = parseInt(rowsLength / MAX_ROWS_TABLE);
    if(numberOfPages === 4) {
        numberOfPages--;
    }
    if (hasMoreRecords || tablePageNumber < numberOfPages) {
        $nextPage.show();
    } else {
        $nextPage.hide();
    }
}

function onChangeDateCallService() {
    clearTransactionsTable();
    hideErrorMessageTransactions();
    var {fromDate, toDate} = getFromToDates();

    if (!fromDate || !toDate || new Date(fromDate) > new Date(toDate)) {
        $('.transparent-transactions .pages-navigator .transaction-next-page').hide();
        $('.transparent-transactions .pages-navigator .transaction-previous-page').hide();
        $(".transparent-transactions .transparent-accounts-errors.transactions-error-date").show();
    } else {
        var transactionsInput = $('#transactionsInput').val();
        servicePageNumber = 0;
        tablePageNumber = 0;

        getTransactionsFromService(fromDate, toDate, transactionsInput);
    }
}

function onClickDisplayTransactionList() {
    $('.transparent-accounts .table-accounts .table-responsive tbody tr td')
        .on('click', function () {
            clearTransactionsTable();
            hideErrorMessageTransactions();
            //clear input search of transactions
            $("#transactionsInput").val("");

            var $tableRow = $(this).parent();
            const accountData = {
                accountOwner: $tableRow.find("td:eq(0)").text(),
                accountIBAN: $tableRow.find("td:eq(1)").text(),
                balance: $tableRow.data("balance"),
                currency: $tableRow.data("currencycode")
            };

            showTransactionsForAccount(accountData, $tableRow.data("accountnumber"));
            setIBANQueryParam(accountData.accountIBAN);
        })
        .on("keypress",function(e){
            if(e.key === "Enter"){
                $(this).click();
            }
        })
}

function clearTransactionsTable() {
    var tableBody = $('.transparent-transactions .table-responsive table tbody');
    tableBody.find("tr:gt(0)").remove();
    return tableBody;
}

function getTransactionsFromService(fromDate, toDate, transactionsInput) {
    var data = getInputDataTransactions(fromDate, toDate, transactionsInput);

    $.ajax({
        type: 'GET',
        url: '/show.pws.transparentTransactions.html',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data: data,
        success: function (data) {
            if (data && data.iHubResponseInfo) {
                if (data.iHubResponseInfo.length > 0) {
                    transparentTransactionsTableRows = data.iHubResponseInfo;
                    hasMoreRecords = data.hasMoreRecords;

                    displayTransactionsTable();
                } else {
                    $('.transparent-transactions .pages-navigator .transaction-next-page').hide();
                    $(".transparent-transactions .transparent-accounts-errors.transactions-no-results").show();
                }
            } else {
                $('.transparent-transactions .pages-navigator .transaction-next-page').hide();
                $(".transparent-transactions .transparent-accounts-errors.transactions-no-results").show();
            }
        },
        error: function () {
            $('.transparent-transactions .pages-navigator .transaction-next-page').hide();
            $(".transparent-transactions .transparent-accounts-errors.transactions-no-results").show();
        }
    });
}

function showTransactionsForAccount(accountData, accountNumber) {
    const { fromDate, toDate } = getDefaultTransactionDateRange();
    populateAccountTransactionsDetailsHeader(accountData);

    servicePageNumber = 0;
    tablePageNumber = 0;

    accountNumberTransactions = accountNumber;
    getTransactionsFromService(fromDate, toDate);

    setDefaultValuesDateInputs();

    $('section.transparent-accounts').hide();
    $('section.transparent-transactions').show();
    $('section.transparent-transactions .transactions-back button').focus();
}

function getInputDataTransactions(fromDate, toDate, transactionsInput) {
    var data = {};

    data.accountNumber = accountNumberTransactions;
    data.dateFrom = fromDate;
    data.dateTo = toDate;
    data.entityCode = $("#transparentAccountEntityCode").val();

    servicePageNumber++;
    if (servicePageNumber > 0) {
        data.pageNumber = servicePageNumber;
    } else {
        data.pageNumber = 1;
    }

    if (transactionsInput) {
        data.transactionsInput = encodeURIComponent(transactionsInput);
    }
    return data;
}

function displayTransactionsTable() {
    var tableBody = clearTransactionsTable();

    var getNewPageFromService = false;
    if(tablePageNumber == 4) {
        getNewPageFromService = true;
        tablePageNumber = 0;
    }
    if(tablePageNumber == -1) {
        getNewPageFromService = true;
        tablePageNumber = 3;
    }

    if (getNewPageFromService) {
        var transactionsInput = $('#transactionsInput').val();
        var {fromDate, toDate} = getFromToDates();
        getTransactionsFromService(fromDate, toDate, transactionsInput);
        return;
    }

    var startIndex = tablePageNumber * MAX_ROWS_TABLE;
    while (startIndex < (tablePageNumber + 1) * MAX_ROWS_TABLE) {
        if (transparentTransactionsTableRows[startIndex]) {
            var row = getRowTransactionsTable(transparentTransactionsTableRows[startIndex]);
            tableBody.append(row);
        }
        startIndex++;
    }

    var $previousPage = $('.transparent-transactions .pages-navigator .transaction-previous-page');
    var $nextPage = $('.transparent-transactions .pages-navigator .transaction-next-page');
    showHideTableButtons($previousPage, $nextPage, transparentTransactionsTableRows.length);
}

function getRowTransactionsTable(transaction) {
    var row = "<tr tabindex='0'><td>" + getTransactionDateTable(transaction.transactionDate) + "</td><td>"
        + getTransactionTypeTable(transaction.transactionType) + "</td><td>"
        + transaction.counterParty + "</td><td>"
        + transaction.transactionDetails + "</td><td class='table-align-center'>"
        + transaction.variableCode + "</td><td class='table-align-center'>"
        + transaction.specificCode + "</td><td  class='table-align-right'>"
        + transaction.amount + " " + transaction.currencyCode + "</td>"
        + "</td></tr>";
    return row;
}

function getTransactionDateTable(transactionDate) {
   const date = new Date(transactionDate);
   const day = String(date.getDate()).padStart(2, '0');
   const month = String(date.getMonth() + 1).padStart(2, '0');
   const year = date.getFullYear();

   return `${day}/${month}/${year}`;
}

function getTransactionTypeTable(transactionType) {
   return window.transactionTypes[transactionType] || "";
}

function hideErrorMessageTransactions() {
    $(".transparent-transactions .transparent-accounts-errors.transactions-error-date").hide();
    $(".transparent-transactions .transparent-accounts-errors.transactions-no-input").hide();
    $(".transparent-transactions .transparent-accounts-errors.transactions-no-results").hide();
}

function getFromToDates() {
    var fromDate = transformToServerFormat($(".date-transactions #datepicker-filter-chart-from").val());
    var toDate = transformToServerFormat($(".date-transactions #datepicker-filter-chart-to").val());
    return {fromDate, toDate};
}

function transformToServerFormat(dateString){
    if (!dateString || dateString.split("/").length !== 3) {
        return null;
    }
    let parts = dateString.split("/");
    return parts[2] + '-' + parts[1] + '-' + parts[0];
}

function setDefaultValuesDateInputs() {
    var now = new Date();
    var prevMonthFirstDate = new Date(now.getFullYear() - (now.getMonth() > 0 ? 0 : 1), (now.getMonth() - 1 + 12) % 12, 1);

    var $fromDate = $(".date-transactions #datepicker-filter-chart-from");
    var $toDate = $(".date-transactions #datepicker-filter-chart-to");

    $fromDate.attr("max", formatDate(now));
    $toDate.attr("max", formatDate(now));

    $fromDate.val(formatDateDayMonthYear(prevMonthFirstDate));
    $toDate.val(formatDateDayMonthYear(now));
}

function formatDate(date) {
    return date.getFullYear() + '-' + formatDateComponent(date.getMonth() + 1) + '-' + formatDateComponent(date.getDate());
}

function formatDateDayMonthYear(date) {
    return formatDateComponent(date.getDate()) + '/' + formatDateComponent(date.getMonth() + 1) + '/' + date.getFullYear();
}

function formatDateComponent(dateComponent) {
    return (dateComponent < 10 ? '0' : '') + dateComponent;
}

function loadTransactionsFromIbanQueryParam() {
    const iban = new URLSearchParams(window.location.search).get('IBAN');

    if (!iban) {
        $('section.transparent-accounts').show();
        return;
    }

    if (iban.length !== 24 || !isValidIban(iban)) {
        $('section.transparent-accounts').show();
        $('.transparent-accounts .transparent-accounts-errors.error-iban').show();
        return;
    }

    getTransactionsFromIbanParam(iban);
}

function getDefaultTransactionDateRange() {
    const now = new Date();

    const prevMonthFirstDate = new Date(
        now.getFullYear() - (now.getMonth() > 0 ? 0 : 1),
        (now.getMonth() - 1 + 12) % 12,
        1
    );

    return {
        fromDate: formatDate(prevMonthFirstDate),
        toDate: formatDate(now)
    };
}

function populateAccountTransactionsDetailsHeader(account) {
    const $info = $(".transparent-transactions .transaction-account-information");

    $info.find(".value-account-owner").text(account.accountOwner);
    $info.find(".value-account-iban").text(account.accountIBAN);
    $info.find(".value-account-amount .amount").text(account.balance);
    $info.find(".value-account-amount .currency-amount")
        .text(" " + (account.currency ?? ""));
}

function getTransactionsFromIbanParam(iban) {
    var data = getInputDataAccounts(undefined, iban);
    $.ajax({
        type: 'GET',
        url: '/show.pws.transparentAccounts.html',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data: data,
        success: function (data) {
            if (data && data.iHubResponseInfo && data.iHubResponseInfo.length === 1) {
                const account = data.iHubResponseInfo[0];
                showTransactionsForAccount(account, account.accountNumber);
            } else {
                $('section.transparent-accounts').show();
                $(".transparent-accounts .transparent-accounts-errors.no-results").show();
            }
        },
        error: function () {
            $('section.transparent-accounts').show();
            $(".transparent-accounts .transparent-accounts-errors.no-results").show();
        }
    });
}

function setIBANQueryParam(iban) {
    const url = new URL(window.location.href);
    url.searchParams.set('IBAN', iban);
    history.replaceState({}, '', url);
}

function removeIBANQueryParam() {
    const url = new URL(window.location.href);
    url.searchParams.delete('IBAN');
    history.replaceState({}, '', url);
}


$('.transparent-transactions .transaction-account-information .copy-url-btn').on('click', async function () {
    const $btn = $(this);
    const $liveRegion = $btn.siblings('.sr-only');

    try {
        const pageUrl = window.location.href;
        await navigator.clipboard.writeText(pageUrl);
        $btn.addClass('copied');
        const successText = $btn.find('.label-copied').text();

        $liveRegion.text('');
        setTimeout(() => {
            $liveRegion.text(successText);
            setTimeout(() => {
                $liveRegion.text('');
            }, 1000);
        }, 50);

        setTimeout(() => {
            $btn.removeClass('copied');
        }, 2000);

    } catch (err) {
        console.error('Copy failed', err);
    }
});