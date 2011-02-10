-- MySQL dump 10.13  Distrib 5.1.47, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: s3u001
-- ------------------------------------------------------
-- Server version	5.1.47

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tabAccount`
--

DROP TABLE IF EXISTS `tabAccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAccount` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_name` varchar(180) DEFAULT NULL,
  `parent_account` varchar(180) DEFAULT NULL,
  `account_type` varchar(180) DEFAULT NULL,
  `tax_rate` decimal(14,2) DEFAULT NULL,
  `group_or_ledger` varchar(180) DEFAULT NULL,
  `is_pl_account` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `debit_or_credit` varchar(180) DEFAULT NULL,
  `balance` decimal(14,2) DEFAULT NULL,
  `balance_as_on` date DEFAULT NULL,
  `old_parent` varchar(180) DEFAULT NULL,
  `lft` int(11) DEFAULT NULL,
  `rgt` int(11) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `pan_number` varchar(180) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  `master_type` varchar(180) DEFAULT NULL,
  `master_name` varchar(180) DEFAULT NULL,
  `address` text,
  `transaction_date` date DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `special_tds_rate` decimal(14,2) DEFAULT NULL,
  `default_tds_category` varchar(180) DEFAULT NULL,
  `tds_applicable` varchar(180) DEFAULT NULL,
  `special_tds_limit` decimal(14,2) DEFAULT NULL,
  `freeze_account` varchar(180) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `sp_tds_rate_applicable` varchar(180) DEFAULT NULL,
  `credit_days` int(11) DEFAULT NULL,
  `credit_limit` decimal(14,2) DEFAULT NULL,
  `cash_flow_level` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `lft` (`lft`),
  KEY `rgt` (`rgt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabAccount Balance`
--

DROP TABLE IF EXISTS `tabAccount Balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAccount Balance` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `opening` decimal(14,2) DEFAULT NULL,
  `balance` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabAdvance Adjustment Detail`
--

DROP TABLE IF EXISTS `tabAdvance Adjustment Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAdvance Adjustment Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `journal_voucher` varchar(180) DEFAULT NULL,
  `adjust_amount` decimal(14,2) DEFAULT NULL,
  `adjust` varchar(180) DEFAULT NULL,
  `remarks` text,
  `jv_detail_no` varchar(180) DEFAULT NULL,
  `allocate` decimal(14,2) DEFAULT NULL,
  `advance_amount` decimal(14,2) DEFAULT NULL,
  `allocated_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabAdvance Allocation Detail`
--

DROP TABLE IF EXISTS `tabAdvance Allocation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAdvance Allocation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `journal_voucher` varchar(180) DEFAULT NULL,
  `jv_detail_no` date DEFAULT NULL,
  `remarks` text,
  `advance_amount` decimal(14,2) DEFAULT NULL,
  `allocated_amount` decimal(14,2) DEFAULT NULL,
  `tds_amount` decimal(14,2) DEFAULT NULL,
  `tds_allocated` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabAnnouncement`
--

DROP TABLE IF EXISTS `tabAnnouncement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAnnouncement` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabApplication`
--

DROP TABLE IF EXISTS `tabApplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabApplication` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `application_name` varchar(180) DEFAULT NULL,
  `description` text,
  `server` varchar(180) DEFAULT NULL,
  `path` varchar(180) DEFAULT NULL,
  `login_id` varchar(180) DEFAULT NULL,
  `password` varchar(180) DEFAULT NULL,
  `account_name` varchar(180) DEFAULT NULL,
  `pwd` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabApplication Type`
--

DROP TABLE IF EXISTS `tabApplication Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabApplication Type` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `type_name` varchar(180) DEFAULT NULL,
  `description` text,
  `source_db` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabApproval Structure`
--

DROP TABLE IF EXISTS `tabApproval Structure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabApproval Structure` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `doctype_name` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `approving_authority` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabArticle`
--

DROP TABLE IF EXISTS `tabArticle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabArticle` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `serial_no` varchar(180) DEFAULT NULL,
  `make` varchar(180) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `pr_no` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `is_cancelled` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `serial_no` (`serial_no`),
  KEY `purchase_date` (`purchase_date`),
  KEY `purchase_rate` (`purchase_rate`),
  KEY `is_cancelled` (`is_cancelled`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabAuthorization Rule`
--

DROP TABLE IF EXISTS `tabAuthorization Rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabAuthorization Rule` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `transaction` varchar(180) DEFAULT NULL,
  `based_on` varchar(180) DEFAULT NULL,
  `master_name` varchar(180) DEFAULT NULL,
  `system_user` varchar(180) DEFAULT NULL,
  `approving_role` varchar(180) DEFAULT NULL,
  `approving_user` varchar(180) DEFAULT NULL,
  `value` decimal(14,2) DEFAULT NULL,
  `cancel_reason` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBOM Material`
--

DROP TABLE IF EXISTS `tabBOM Material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBOM Material` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `operation_no` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `bom_no` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `scrap` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `direct_material` decimal(14,2) DEFAULT NULL,
  `operating_cost` decimal(14,2) DEFAULT NULL,
  `direct_labour` decimal(14,2) DEFAULT NULL,
  `direct_overhead` decimal(14,2) DEFAULT NULL,
  `value` decimal(14,2) DEFAULT NULL,
  `moving_avg_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `qty_consumed_per_fg` decimal(14,2) DEFAULT NULL,
  `last_purchase_rate` decimal(14,2) DEFAULT NULL,
  `pro_applicable` varchar(180) DEFAULT NULL,
  `qty_consumed_per_unit` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_mar` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_sr` decimal(14,2) DEFAULT NULL,
  `value_as_per_mar` decimal(14,2) DEFAULT NULL,
  `value_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `value_as_per_sr` decimal(14,2) DEFAULT NULL,
  `amount_as_per_mar` decimal(14,2) DEFAULT NULL,
  `amount_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `standard_rate` decimal(14,2) DEFAULT NULL,
  `amount_as_per_sr` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `bom_no` (`bom_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBOM Operation`
--

DROP TABLE IF EXISTS `tabBOM Operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBOM Operation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `operation_no` varchar(180) DEFAULT NULL,
  `operation_type` varchar(180) DEFAULT NULL,
  `opn_description` text,
  `details` varchar(180) DEFAULT NULL,
  `workstation` varchar(180) DEFAULT NULL,
  `hour_rate` decimal(14,2) DEFAULT NULL,
  `workstation_capacity` decimal(14,2) DEFAULT NULL,
  `capacity_units` varchar(180) DEFAULT NULL,
  `time_in_mins` decimal(14,2) DEFAULT NULL,
  `operating_cost` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBOM Replace Utility Detail`
--

DROP TABLE IF EXISTS `tabBOM Replace Utility Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBOM Replace Utility Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `parent_bom` varchar(180) DEFAULT NULL,
  `replace` int(3) DEFAULT NULL,
  `bom_created` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBOM Report Detail`
--

DROP TABLE IF EXISTS `tabBOM Report Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBOM Report Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` varchar(180) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `moving_avg_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `last_purchase_rate` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBank Reconciliation Detail`
--

DROP TABLE IF EXISTS `tabBank Reconciliation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBank Reconciliation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `voucher_id` varchar(180) DEFAULT NULL,
  `cheque_number` varchar(180) DEFAULT NULL,
  `cheque_date` date DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `type` varchar(180) DEFAULT NULL,
  `clearance_date` date DEFAULT NULL,
  `against_account` varchar(180) DEFAULT NULL,
  `voucher_date` date DEFAULT NULL,
  `debit` decimal(14,2) DEFAULT NULL,
  `credit` decimal(14,2) DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBill Of Materials`
--

DROP TABLE IF EXISTS `tabBill Of Materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBill Of Materials` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item` varchar(180) DEFAULT NULL,
  `old_code` varchar(180) DEFAULT NULL,
  `description` text,
  `quantity` decimal(14,6) DEFAULT NULL,
  `version` varchar(180) DEFAULT NULL,
  `version_date` date DEFAULT NULL,
  `is_default` int(3) DEFAULT NULL,
  `discontinued` int(3) DEFAULT NULL,
  `bom_date` date DEFAULT NULL,
  `remarks` text,
  `cost` decimal(14,2) DEFAULT NULL,
  `cost_as_on` varchar(180) DEFAULT NULL,
  `direct_material` decimal(14,2) DEFAULT NULL,
  `operating_cost` decimal(14,2) DEFAULT NULL,
  `direct_labour` decimal(14,2) DEFAULT NULL,
  `direct_overhead` decimal(14,2) DEFAULT NULL,
  `maintained_by` varchar(180) DEFAULT NULL,
  `prev_direct_material` decimal(14,2) DEFAULT NULL,
  `prev_operating_cost` decimal(14,2) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `is_sub_assembly` varchar(180) DEFAULT NULL,
  `cost_as_per_mar` decimal(14,2) DEFAULT NULL,
  `cost_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `cost_as_per_sr` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_mar` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `dir_mat_as_per_sr` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item` (`item`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBin`
--

DROP TABLE IF EXISTS `tabBin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBin` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `reserved_qty` decimal(14,2) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `ordered_qty` decimal(14,2) DEFAULT NULL,
  `indented_qty` decimal(14,2) DEFAULT NULL,
  `available_qty` decimal(14,2) DEFAULT NULL,
  `ma_rate` decimal(14,2) DEFAULT NULL,
  `fcfs_rate` decimal(14,2) DEFAULT NULL,
  `projected_qty` decimal(14,2) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `warehouse_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `warehouse` (`warehouse`),
  KEY `item_code` (`item_code`),
  KEY `available_qty` (`available_qty`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBrand`
--

DROP TABLE IF EXISTS `tabBrand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBrand` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBudget Detail`
--

DROP TABLE IF EXISTS `tabBudget Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBudget Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account` varchar(180) DEFAULT NULL,
  `budget_allocated` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  `distribution_id` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `account` (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBudget Distribution`
--

DROP TABLE IF EXISTS `tabBudget Distribution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBudget Distribution` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `distribution_id` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabBudget Distribution Detail`
--

DROP TABLE IF EXISTS `tabBudget Distribution Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabBudget Distribution Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `percentage_allocation` decimal(14,2) DEFAULT NULL,
  `aggregate_percentage` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCampaign`
--

DROP TABLE IF EXISTS `tabCampaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCampaign` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `campaign_name` varchar(180) DEFAULT NULL,
  `campaign_details` text,
  `status` varchar(180) DEFAULT NULL,
  `total_campaign_investment` decimal(14,2) DEFAULT NULL,
  `campaign_revenue` decimal(14,2) DEFAULT NULL,
  `gross_rate` decimal(14,2) DEFAULT NULL,
  `gross_income` decimal(14,2) DEFAULT NULL,
  `net_income` decimal(14,2) DEFAULT NULL,
  `campaign_roi` decimal(14,2) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCampaign Expense`
--

DROP TABLE IF EXISTS `tabCampaign Expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCampaign Expense` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `description` text,
  `rate` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabChange Log`
--

DROP TABLE IF EXISTS `tabChange Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabChange Log` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `by` varchar(180) DEFAULT NULL,
  `description` text,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCode History`
--

DROP TABLE IF EXISTS `tabCode History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCode History` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `script_from` varchar(180) DEFAULT NULL,
  `record_id` varchar(180) DEFAULT NULL,
  `field_name` varchar(180) DEFAULT NULL,
  `comment` text,
  `code` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `script_from` (`script_from`),
  KEY `record_id` (`record_id`),
  KEY `field_name` (`field_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCompany`
--

DROP TABLE IF EXISTS `tabCompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCompany` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `abbr` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `default_bank_account` varchar(180) DEFAULT NULL,
  `receivables_group` varchar(180) DEFAULT NULL,
  `payables_group` varchar(180) DEFAULT NULL,
  `pan_no` varchar(180) DEFAULT NULL,
  `tan_no` varchar(180) DEFAULT NULL,
  `address` text,
  `letter_head` text,
  `if_budget_exceeded` varchar(180) DEFAULT NULL,
  `yearly_budget_exceeded` varchar(180) DEFAULT NULL,
  `credit_days` int(11) DEFAULT NULL,
  `credit_limit` decimal(14,2) DEFAULT NULL,
  `yearly_bgt_flag` varchar(180) DEFAULT NULL,
  `monthly_bgt_flag` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCompetitor`
--

DROP TABLE IF EXISTS `tabCompetitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCompetitor` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `competitor_name` varchar(180) DEFAULT NULL,
  `product_family` varchar(180) DEFAULT NULL,
  `market_segment` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `contact_numer` varchar(180) DEFAULT NULL,
  `address` text,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `strengths` text,
  `weaknesses` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabComplaint Detail`
--

DROP TABLE IF EXISTS `tabComplaint Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabComplaint Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `issue_description` text,
  `issue_updates` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabComplaint Note`
--

DROP TABLE IF EXISTS `tabComplaint Note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabComplaint Note` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_type` varchar(180) DEFAULT NULL,
  `customer_ref` varchar(180) DEFAULT NULL,
  `customer_address` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `call_type` varchar(180) DEFAULT NULL,
  `call_against` varchar(180) DEFAULT NULL,
  `so_id` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `complaint_date` date DEFAULT NULL,
  `note` text,
  `naming_series` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `complaint_type` varchar(180) DEFAULT NULL,
  `complaint_raised_by` varchar(180) DEFAULT NULL,
  `allocated_on` date DEFAULT NULL,
  `allocated_to` varchar(180) DEFAULT NULL,
  `resolution_date` date DEFAULT NULL,
  `resolved_by` varchar(180) DEFAULT NULL,
  `resolution_details` text,
  `quotation_no` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `customer_name` (`customer_name`),
  KEY `status` (`status`),
  KEY `complaint_date` (`complaint_date`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `territory` (`territory`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabComplaint Note Detail`
--

DROP TABLE IF EXISTS `tabComplaint Note Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabComplaint Note Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `product` varchar(180) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  `remark` text,
  `nature_of_complaint` text,
  `call_attnd_date` date DEFAULT NULL,
  `call_complete_date` date DEFAULT NULL,
  `technician` varchar(180) DEFAULT NULL,
  `technician_2` varchar(180) DEFAULT NULL,
  `no_of_visit` int(11) DEFAULT NULL,
  `technician_available` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabContact`
--

DROP TABLE IF EXISTS `tabContact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabContact` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `contact_name` varchar(180) DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `address` text,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `via_campaign` varchar(180) DEFAULT NULL,
  `market_segment` varchar(180) DEFAULT NULL,
  `telephone` text,
  `work_phone` varchar(180) DEFAULT NULL,
  `cell_number` varchar(180) DEFAULT NULL,
  `home_phone` varchar(180) DEFAULT NULL,
  `close_contact` int(3) DEFAULT NULL,
  `contact_type` varchar(180) DEFAULT NULL,
  `is_supplier` int(3) DEFAULT NULL,
  `supplier_name` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `is_customer` int(3) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_address` text,
  `is_sales_partner` int(3) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `sales_partner_address` text,
  `company_name` varchar(180) DEFAULT NULL,
  `company_address` text,
  `first_name` varchar(180) DEFAULT NULL,
  `last_name` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `contact_address` text,
  `has_login` varchar(180) DEFAULT NULL,
  `disable_login` varchar(180) DEFAULT NULL,
  `supplier_type` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `partner_type` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `is_primary_contact` varchar(180) DEFAULT NULL,
  `mobile_no` varchar(180) DEFAULT NULL,
  `fax` varchar(180) DEFAULT NULL,
  `email_id2` varchar(180) DEFAULT NULL,
  `email_id1` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabContact Detail`
--

DROP TABLE IF EXISTS `tabContact Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabContact Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `email_id` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCost Center`
--

DROP TABLE IF EXISTS `tabCost Center`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCost Center` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `cost_center_name` varchar(180) DEFAULT NULL,
  `parent_cost_center` varchar(180) DEFAULT NULL,
  `debit_or_credit` varchar(180) DEFAULT NULL,
  `balance` decimal(14,2) DEFAULT NULL,
  `balance_as_on` date DEFAULT NULL,
  `lft` int(11) DEFAULT NULL,
  `rgt` int(11) DEFAULT NULL,
  `old_parent` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `is_group` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `group_or_ledger` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `lft` (`lft`),
  KEY `rgt` (`rgt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCost Center Balance`
--

DROP TABLE IF EXISTS `tabCost Center Balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCost Center Balance` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `opening` decimal(14,2) DEFAULT NULL,
  `balance` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCountry`
--

DROP TABLE IF EXISTS `tabCountry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCountry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `country_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCurrency`
--

DROP TABLE IF EXISTS `tabCurrency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCurrency` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `currency_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCustomer`
--

DROP TABLE IF EXISTS `tabCustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCustomer` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `region` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `customer_ref` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `phone_1` varchar(180) DEFAULT NULL,
  `phone_2` varchar(180) DEFAULT NULL,
  `fax_1` varchar(180) DEFAULT NULL,
  `mobile_1` varchar(180) DEFAULT NULL,
  `email_1` varchar(180) DEFAULT NULL,
  `website` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `credit_limit` decimal(14,2) DEFAULT NULL,
  `address` text,
  `telephone` text,
  `account_head` varchar(180) DEFAULT NULL,
  `authorization_document` varchar(180) DEFAULT NULL,
  `last_sales_order` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `lead_name` varchar(180) DEFAULT NULL,
  `tin_no` varchar(180) DEFAULT NULL,
  `cst_tin` varchar(180) DEFAULT NULL,
  `vat_tin_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `customer_name` (`customer_name`),
  KEY `territory` (`territory`),
  KEY `company` (`company`),
  KEY `zone` (`zone`),
  KEY `country` (`country`),
  KEY `state` (`state`),
  KEY `customer_group` (`customer_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCustomer Group`
--

DROP TABLE IF EXISTS `tabCustomer Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCustomer Group` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `group_name` varchar(180) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabCustomer Issue`
--

DROP TABLE IF EXISTS `tabCustomer Issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabCustomer Issue` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `issue_raised_by` varchar(180) DEFAULT NULL,
  `attended_by` varchar(180) DEFAULT NULL,
  `complaint_date` date DEFAULT NULL,
  `resolved_date` date DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `issue_against` varchar(180) DEFAULT NULL,
  `sales_order_id` varchar(180) DEFAULT NULL,
  `assigned_to` varchar(180) DEFAULT NULL,
  `first_creation_flag` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDAR`
--

DROP TABLE IF EXISTS `tabDAR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDAR` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `dar_date` date DEFAULT NULL,
  `product_code` varchar(180) DEFAULT NULL,
  `product_description` text,
  `from` varchar(180) DEFAULT NULL,
  `ch_date` date DEFAULT NULL,
  `deviation_details` text,
  `reason_for_acceptance` text,
  `request_accepted` text,
  `design_approval` text,
  `dar_closed_on` date DEFAULT NULL,
  `qa_inspector` varchar(180) DEFAULT NULL,
  `iso_no` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDCR`
--

DROP TABLE IF EXISTS `tabDCR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDCR` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `dcr_date` date DEFAULT NULL,
  `from` varchar(180) DEFAULT NULL,
  `ammended_from` varchar(180) DEFAULT NULL,
  `ammendment_date` date DEFAULT NULL,
  `originator` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `product_code` varchar(180) DEFAULT NULL,
  `product_description` text,
  `drawing_no` varchar(180) DEFAULT NULL,
  `reason_for_hanges` varchar(180) DEFAULT NULL,
  `proposed_modification` text,
  `request_accepted` text,
  `tcn_no` varchar(180) DEFAULT NULL,
  `pcn_no` varchar(180) DEFAULT NULL,
  `regret` varchar(180) DEFAULT NULL,
  `design_remarks` text,
  `iso_no` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDefault Home Page`
--

DROP TABLE IF EXISTS `tabDefault Home Page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDefault Home Page` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  `home_page` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDefaultValue`
--

DROP TABLE IF EXISTS `tabDefaultValue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDefaultValue` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `defkey` varchar(180) DEFAULT NULL,
  `defvalue` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDelivery Note`
--

DROP TABLE IF EXISTS `tabDelivery Note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDelivery Note` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `delivery_type` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `posting_time` time DEFAULT NULL,
  `po_no` varchar(180) DEFAULT NULL,
  `po_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_address` text,
  `zone` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `total_commission` decimal(14,2) DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `note` text,
  `internal_note` text,
  `transporter_name` varchar(180) DEFAULT NULL,
  `lr_no` varchar(180) DEFAULT NULL,
  `lr_date` date DEFAULT NULL,
  `sales_order_no` varchar(180) DEFAULT NULL,
  `purchase_receipt_no` varchar(180) DEFAULT NULL,
  `purchase_order_no` varchar(180) DEFAULT NULL,
  `to_warehouse` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  `naming_series` varchar(180) DEFAULT NULL,
  `ref_rate_total` decimal(14,2) DEFAULT NULL,
  `total_discount` decimal(14,2) DEFAULT NULL,
  `total_discount_rate` decimal(14,2) DEFAULT NULL,
  `delivery_address` text,
  `charge` varchar(180) DEFAULT NULL,
  `activity_log_text` text,
  `consignee_address` text,
  `vehicle_no` varchar(180) DEFAULT NULL,
  `mode_of_transport` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `time_of_issue` varchar(180) DEFAULT NULL,
  `date_of_issue` date DEFAULT NULL,
  `date_of_removal` date DEFAULT NULL,
  `time_of_removal` varchar(180) DEFAULT NULL,
  `excise_duty_paid` decimal(14,2) DEFAULT NULL,
  `excise_duty_in_words` text,
  `bills_through` varchar(180) DEFAULT NULL,
  `billing_address` text,
  `billing_name` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `phone_1` varchar(180) DEFAULT NULL,
  `email_1` varchar(180) DEFAULT NULL,
  `sales_order_date` date DEFAULT NULL,
  `concluding_note` text,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `gross_profit` decimal(14,2) DEFAULT NULL,
  `gross_profit_percent` decimal(14,2) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  `commission_applicable` varchar(180) DEFAULT NULL,
  `discount_rate` decimal(14,2) DEFAULT NULL,
  `cash_discount_rate` decimal(14,2) DEFAULT NULL,
  `net_discount` decimal(14,2) DEFAULT NULL,
  `gross_amt` decimal(14,2) DEFAULT NULL,
  `cash_discount_amt` decimal(14,2) DEFAULT NULL,
  `work_order_value` decimal(14,2) DEFAULT NULL,
  `per_on_ref_rate_total` decimal(14,2) DEFAULT NULL,
  `price_list_value` decimal(14,2) DEFAULT NULL,
  `commission_amt` decimal(14,2) DEFAULT NULL,
  `amount_for_incentive` decimal(14,2) DEFAULT NULL,
  `rate_of_dis_saving` decimal(14,2) DEFAULT NULL,
  `total_incentive` decimal(14,2) DEFAULT NULL,
  `total_commission_amount` decimal(14,2) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `excise_page` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `per_billed` varchar(180) DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `campaign` varchar(180) DEFAULT NULL,
  `per_installed` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `delivery_type` (`delivery_type`),
  KEY `transaction_date` (`transaction_date`),
  KEY `posting_date` (`posting_date`),
  KEY `customer_name` (`customer_name`),
  KEY `department` (`department`),
  KEY `city` (`city`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `chargeable` (`chargeable`),
  KEY `state` (`state`),
  KEY `per_billed` (`per_billed`),
  KEY `per_installed` (`per_installed`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDelivery Note Detail`
--

DROP TABLE IF EXISTS `tabDelivery Note Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDelivery Note Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `description` text,
  `article_no` text,
  `no_of_packs` int(11) DEFAULT NULL,
  `pack_unit` varchar(180) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `adj_rate` decimal(14,6) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `colour` varchar(180) DEFAULT NULL,
  `item_tax_rate` text,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `total_tax_amount` decimal(14,2) DEFAULT NULL,
  `billed_qty` decimal(14,2) DEFAULT NULL,
  `print_rate` decimal(14,2) DEFAULT NULL,
  `print_amount` decimal(14,2) DEFAULT NULL,
  `print_amt` decimal(14,2) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `serial_no` text,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `excise_category` varchar(180) DEFAULT NULL,
  `installed_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `prevdoc_docname` (`prevdoc_docname`),
  KEY `prevdoc_doctype` (`prevdoc_doctype`),
  KEY `prevdoc_detail_docname` (`prevdoc_detail_docname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDelivery Note Packing Detail`
--

DROP TABLE IF EXISTS `tabDelivery Note Packing Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDelivery Note Packing Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `parent_item` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `parent_detail_docname` varchar(180) DEFAULT NULL,
  `discount` decimal(14,2) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDocField`
--

DROP TABLE IF EXISTS `tabDocField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDocField` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `fieldname` varchar(180) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `oldfieldname` varchar(180) DEFAULT NULL,
  `fieldtype` varchar(180) DEFAULT NULL,
  `oldfieldtype` varchar(180) DEFAULT NULL,
  `options` text,
  `search_index` int(3) DEFAULT NULL,
  `hidden` int(3) DEFAULT NULL,
  `print_hide` int(3) DEFAULT NULL,
  `report_hide` int(3) DEFAULT NULL,
  `reqd` int(3) DEFAULT NULL,
  `no_copy` int(3) DEFAULT NULL,
  `allow_on_submit` int(3) DEFAULT NULL,
  `trigger` varchar(180) DEFAULT NULL,
  `depends_on` varchar(180) DEFAULT NULL,
  `permlevel` int(3) DEFAULT NULL,
  `width` varchar(180) DEFAULT NULL,
  `default` text,
  `description` text,
  `colour` varchar(180) DEFAULT NULL,
  `icon` varchar(180) DEFAULT NULL,
  `in_filter` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `label` (`label`),
  KEY `fieldtype` (`fieldtype`),
  KEY `fieldname` (`fieldname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDocFormat`
--

DROP TABLE IF EXISTS `tabDocFormat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDocFormat` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `format` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDocPerm`
--

DROP TABLE IF EXISTS `tabDocPerm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDocPerm` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `permlevel` int(11) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  `match` varchar(180) DEFAULT NULL,
  `read` int(3) DEFAULT NULL,
  `write` int(3) DEFAULT NULL,
  `create` int(3) DEFAULT NULL,
  `submit` int(3) DEFAULT NULL,
  `cancel` int(3) DEFAULT NULL,
  `amend` int(3) DEFAULT NULL,
  `execute` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `permlevel` (`permlevel`),
  KEY `role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDocType`
--

DROP TABLE IF EXISTS `tabDocType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDocType` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `search_fields` varchar(180) DEFAULT NULL,
  `issingle` int(3) DEFAULT NULL,
  `istable` int(3) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  `autoname` varchar(180) DEFAULT NULL,
  `name_case` varchar(180) DEFAULT NULL,
  `description` text,
  `colour` varchar(180) DEFAULT NULL,
  `read_only` int(3) DEFAULT NULL,
  `in_create` int(3) DEFAULT NULL,
  `show_in_menu` int(3) DEFAULT NULL,
  `menu_index` int(11) DEFAULT NULL,
  `parent_node` varchar(180) DEFAULT NULL,
  `smallicon` varchar(180) DEFAULT NULL,
  `allow_print` int(3) DEFAULT NULL,
  `allow_email` int(3) DEFAULT NULL,
  `allow_copy` int(3) DEFAULT NULL,
  `allow_rename` int(3) DEFAULT NULL,
  `hide_toolbar` int(3) DEFAULT NULL,
  `hide_heading` int(3) DEFAULT NULL,
  `allow_attach` int(3) DEFAULT NULL,
  `use_template` int(3) DEFAULT NULL,
  `max_attachments` int(11) DEFAULT NULL,
  `section_style` varchar(180) DEFAULT NULL,
  `client_script` text,
  `client_script_core` text,
  `server_code` text,
  `server_code_core` text,
  `server_code_compiled` text,
  `client_string` text,
  `server_code_error` text,
  `print_outline` varchar(180) DEFAULT NULL,
  `dt_template` text,
  `version` int(11) DEFAULT NULL,
  `change_log` text,
  `is_transaction_doc` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `module` (`module`),
  KEY `istable` (`istable`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabDocType Mapper`
--

DROP TABLE IF EXISTS `tabDocType Mapper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabDocType Mapper` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  `from_doctype` varchar(180) DEFAULT NULL,
  `to_doctype` varchar(180) DEFAULT NULL,
  `ref_doc_submitted` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEMP Deduction Detail`
--

DROP TABLE IF EXISTS `tabEMP Deduction Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEMP Deduction Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `account_name` varchar(180) DEFAULT NULL,
  `alias_account_head` varchar(180) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `amount` (`amount`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEMP Earning Detail`
--

DROP TABLE IF EXISTS `tabEMP Earning Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEMP Earning Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `account_name` varchar(180) DEFAULT NULL,
  `alias_account_head` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `account_head` (`account_head`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEmployee`
--

DROP TABLE IF EXISTS `tabEmployee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEmployee` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `employee_code` varchar(180) DEFAULT NULL,
  `first_name` varchar(180) DEFAULT NULL,
  `second_name` varchar(180) DEFAULT NULL,
  `last_name` varchar(180) DEFAULT NULL,
  `gender` varchar(180) DEFAULT NULL,
  `marital_status` varchar(180) DEFAULT NULL,
  `no_of_children` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `branch` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `grade` varchar(180) DEFAULT NULL,
  `reports_to` varchar(180) DEFAULT NULL,
  `is_permanent` varchar(180) DEFAULT NULL,
  `is_sales_agent` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `date_of_joining` date DEFAULT NULL,
  `date_of_leaving` date DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `pan_no` varchar(180) DEFAULT NULL,
  `education` varchar(180) DEFAULT NULL,
  `bank_branch` varchar(180) DEFAULT NULL,
  `bank_name` varchar(180) DEFAULT NULL,
  `bank_a/c_no` varchar(180) DEFAULT NULL,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pincode` int(11) DEFAULT NULL,
  `phone_no` int(11) DEFAULT NULL,
  `mobile_no` int(11) DEFAULT NULL,
  `fax` int(11) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `approves_advances` varchar(180) DEFAULT NULL,
  `approves_expenses` varchar(180) DEFAULT NULL,
  `carry_forward_leave` decimal(14,6) DEFAULT NULL,
  `basic_salary` decimal(14,2) DEFAULT NULL,
  `provident_fund` decimal(14,2) DEFAULT NULL,
  `professional_tax` decimal(14,2) DEFAULT NULL,
  `salary_for` varchar(180) DEFAULT NULL,
  `ctc` varchar(180) DEFAULT NULL,
  `max_advance` int(11) DEFAULT NULL,
  `alias_cost_center` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `pf_number` varchar(180) DEFAULT NULL,
  `previous_work_details` text,
  `company_name` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `first_name` (`first_name`),
  KEY `cost_center` (`cost_center`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEnquiry`
--

DROP TABLE IF EXISTS `tabEnquiry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEnquiry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `campaign` varchar(180) DEFAULT NULL,
  `lead_name` varchar(180) DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `address` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `contact_by` varchar(180) DEFAULT NULL,
  `contact_date` date DEFAULT NULL,
  `last_contact_date` date DEFAULT NULL,
  `contact_date_ref` date DEFAULT NULL,
  `to_discuss` text,
  `email_id1` varchar(180) DEFAULT NULL,
  `cc_to` varchar(180) DEFAULT NULL,
  `subject` varchar(180) DEFAULT NULL,
  `message` text,
  `sms_message` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEnquiry Attachment Detail`
--

DROP TABLE IF EXISTS `tabEnquiry Attachment Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEnquiry Attachment Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `select_file` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEnquiry Detail`
--

DROP TABLE IF EXISTS `tabEnquiry Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEnquiry Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `product_name` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `lead_time_date` date DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `price` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `min_order_qty` decimal(14,2) DEFAULT NULL,
  `available_qty` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `quantity` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEnquiry SMS Detail`
--

DROP TABLE IF EXISTS `tabEnquiry SMS Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEnquiry SMS Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `other_mobile_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEvent`
--

DROP TABLE IF EXISTS `tabEvent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEvent` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_hour` time DEFAULT NULL,
  `description` text,
  `notes` text,
  `event_type` varchar(180) DEFAULT NULL,
  `ref_type` varchar(180) DEFAULT NULL,
  `ref_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `event_date` (`event_date`),
  KEY `event_type` (`event_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEvent Role`
--

DROP TABLE IF EXISTS `tabEvent Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEvent Role` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabEvent User`
--

DROP TABLE IF EXISTS `tabEvent User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabEvent User` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `person` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `person` (`person`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFeed Control`
--

DROP TABLE IF EXISTS `tabFeed Control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFeed Control` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFeed List`
--

DROP TABLE IF EXISTS `tabFeed List`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFeed List` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `updated_by` varchar(180) DEFAULT NULL,
  `update_date` date DEFAULT NULL,
  `for_role` varchar(180) DEFAULT NULL,
  `doctype_name` varchar(180) DEFAULT NULL,
  `record_no` varchar(180) DEFAULT NULL,
  `for_party` varchar(180) DEFAULT NULL,
  `grand_total` varchar(180) DEFAULT NULL,
  `currency_type` varchar(180) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `feed_event` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabField Mapper Detail`
--

DROP TABLE IF EXISTS `tabField Mapper Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabField Mapper Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `from_field` varchar(180) DEFAULT NULL,
  `to_field` varchar(180) DEFAULT NULL,
  `match_id` int(11) DEFAULT NULL,
  `map` varchar(180) DEFAULT NULL,
  `checking_operator` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFile`
--

DROP TABLE IF EXISTS `tabFile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFile` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `file_name` varchar(180) DEFAULT NULL,
  `description` text,
  `mime_type` varchar(180) DEFAULT NULL,
  `type` varchar(180) DEFAULT NULL,
  `file_group` varchar(180) DEFAULT NULL,
  `file_list` text,
  `shared_with` text,
  `can_edit` text,
  `can_view` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFile Data`
--

DROP TABLE IF EXISTS `tabFile Data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFile Data` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `file_name` varchar(180) DEFAULT NULL,
  `blob_content` longblob,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFile Group`
--

DROP TABLE IF EXISTS `tabFile Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFile Group` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `group_name` varchar(180) DEFAULT NULL,
  `description` text,
  `parent_group` varchar(180) DEFAULT NULL,
  `is_parent` int(3) DEFAULT NULL,
  `shared_with` text,
  `can_edit` text,
  `can_view` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFiscal Year`
--

DROP TABLE IF EXISTS `tabFiscal Year`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFiscal Year` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `year` varchar(180) DEFAULT NULL,
  `year_start_date` date DEFAULT NULL,
  `past_year` varchar(180) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `percent_complete` int(11) DEFAULT NULL,
  `abbreviation` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFlat BOM Detail`
--

DROP TABLE IF EXISTS `tabFlat BOM Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFlat BOM Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `moving_avg_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `last_purchase_rate` decimal(14,2) DEFAULT NULL,
  `qty_consumed_per_unit` decimal(14,2) DEFAULT NULL,
  `flat_bom_no` varchar(180) DEFAULT NULL,
  `bom_mat_no` varchar(180) DEFAULT NULL,
  `parent_bom` varchar(180) DEFAULT NULL,
  `amount_as_per_mar` decimal(14,2) DEFAULT NULL,
  `amount_as_per_lpr` decimal(14,2) DEFAULT NULL,
  `standard_rate` decimal(14,2) DEFAULT NULL,
  `amount_as_per_sr` decimal(14,2) DEFAULT NULL,
  `is_pro_applicable` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFollow up`
--

DROP TABLE IF EXISTS `tabFollow up`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFollow up` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `notes` text,
  `follow_up_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabForm 16A`
--

DROP TABLE IF EXISTS `tabForm 16A`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabForm 16A` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `company_address` text,
  `pan_no` varchar(180) DEFAULT NULL,
  `tan_no` varchar(180) DEFAULT NULL,
  `party_name` varchar(180) DEFAULT NULL,
  `party_address` text,
  `party_pan` varchar(180) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `place` varchar(180) DEFAULT NULL,
  `dt` date DEFAULT NULL,
  `full_name` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabForm 16A Ack Detail`
--

DROP TABLE IF EXISTS `tabForm 16A Ack Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabForm 16A Ack Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `quarter` varchar(180) DEFAULT NULL,
  `ack_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabForm 16A Tax Detail`
--

DROP TABLE IF EXISTS `tabForm 16A Tax Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabForm 16A Tax Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `amount_paid` decimal(14,2) DEFAULT NULL,
  `date_of_payment` date DEFAULT NULL,
  `tds_main` decimal(14,2) DEFAULT NULL,
  `surcharge` decimal(14,2) DEFAULT NULL,
  `edu_cess` decimal(14,2) DEFAULT NULL,
  `sh_edu_cess` decimal(14,2) DEFAULT NULL,
  `total_tax_deposited` decimal(14,2) DEFAULT NULL,
  `cheque_no` varchar(180) DEFAULT NULL,
  `bsr_code` varchar(180) DEFAULT NULL,
  `tax_deposited_date` date DEFAULT NULL,
  `challan_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabForm Settings`
--

DROP TABLE IF EXISTS `tabForm Settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabForm Settings` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `doctype_name` varchar(180) DEFAULT NULL,
  `is_master` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFormica`
--

DROP TABLE IF EXISTS `tabFormica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFormica` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabFreigh Payment`
--

DROP TABLE IF EXISTS `tabFreigh Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabFreigh Payment` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `address` text,
  `contact_person` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `remarks` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `bill_no.` varchar(180) DEFAULT NULL,
  `transporter_name` varchar(180) DEFAULT NULL,
  `payment_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `customer_name` (`customer_name`),
  KEY `delivery_note_no` (`delivery_note_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabGL Entry`
--

DROP TABLE IF EXISTS `tabGL Entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabGL Entry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `account` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `debit` decimal(14,2) DEFAULT NULL,
  `credit` decimal(14,2) DEFAULT NULL,
  `against` text,
  `against_voucher` varchar(180) DEFAULT NULL,
  `against_voucher_type` varchar(180) DEFAULT NULL,
  `voucher_type` varchar(180) DEFAULT NULL,
  `voucher_no` varchar(180) DEFAULT NULL,
  `remarks` text,
  `is_cancelled` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `is_opening` varchar(180) DEFAULT NULL,
  `previous_closing_balance` decimal(14,2) DEFAULT NULL,
  `is_advance` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `account` (`account`),
  KEY `is_opening` (`is_opening`),
  KEY `voucher_no` (`voucher_no`),
  KEY `posting_date` (`posting_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabGL Mapper`
--

DROP TABLE IF EXISTS `tabGL Mapper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabGL Mapper` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `doc_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabGL Mapper Detail`
--

DROP TABLE IF EXISTS `tabGL Mapper Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabGL Mapper Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `table_field` varchar(180) DEFAULT NULL,
  `account` varchar(180) DEFAULT NULL,
  `debit` varchar(180) DEFAULT NULL,
  `credit` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `against` varchar(180) DEFAULT NULL,
  `remarks` varchar(180) DEFAULT NULL,
  `voucher_type` varchar(180) DEFAULT NULL,
  `voucher_no` varchar(180) DEFAULT NULL,
  `posting_date` varchar(180) DEFAULT NULL,
  `transaction_date` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `against_voucher` varchar(180) DEFAULT NULL,
  `against_voucher_type` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `is_opening` varchar(180) DEFAULT NULL,
  `is_advance` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabHomePage Settings`
--

DROP TABLE IF EXISTS `tabHomePage Settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabHomePage Settings` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `doctype_name` varchar(180) DEFAULT NULL,
  `is_master` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabImpact Analysis`
--

DROP TABLE IF EXISTS `tabImpact Analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabImpact Analysis` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `change_title` varchar(180) DEFAULT NULL,
  `analysis_verified_by` varchar(180) DEFAULT NULL,
  `code_verified_by` varchar(180) DEFAULT NULL,
  `related_doctype` text,
  `changes_to_be_made` text,
  `effect_on_existing_account` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabIndent`
--

DROP TABLE IF EXISTS `tabIndent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabIndent` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `is_auto_generated` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `requested_by` varchar(180) DEFAULT NULL,
  `sales_order_no` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `remark` text,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `approved` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `approval_comment` text,
  `activity_log_text` text,
  `order_from` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `required_for` varchar(180) DEFAULT NULL,
  `approval_status` varchar(180) DEFAULT NULL,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `per_ordered` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabIndent Detail`
--

DROP TABLE IF EXISTS `tabIndent Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabIndent Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `lead_time` int(11) DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `min_order_qty` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `ordered_qty` decimal(14,2) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `lead_time_date` date DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `clear_pending` int(3) DEFAULT NULL,
  `available_qty` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `projected_qty` decimal(14,2) DEFAULT NULL,
  `old_uom` varchar(180) DEFAULT NULL,
  `old_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `pending_qty` (`pending_qty`),
  KEY `item_name` (`item_name`),
  KEY `item_group` (`item_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabInstallation Note`
--

DROP TABLE IF EXISTS `tabInstallation Note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabInstallation Note` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `address` text,
  `contact_person` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `inst_date` date DEFAULT NULL,
  `inst_time` text,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `remarks` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `no_of_visit` int(11) DEFAULT NULL,
  `spares_required` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `customer_name` (`customer_name`),
  KEY `delivery_note_no` (`delivery_note_no`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabInstallation Technician Detals`
--

DROP TABLE IF EXISTS `tabInstallation Technician Detals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabInstallation Technician Detals` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `technician` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabInstalled Item Details`
--

DROP TABLE IF EXISTS `tabInstalled Item Details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabInstalled Item Details` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` varchar(180) DEFAULT NULL,
  `prevdoc_date` date DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `serial_no` text,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `prevdoc_docname` (`prevdoc_docname`),
  KEY `prevdoc_doctype` (`prevdoc_doctype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem`
--

DROP TABLE IF EXISTS `tabItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` text,
  `is_active` varchar(180) DEFAULT NULL,
  `make` varchar(180) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `description` text,
  `long_description` text,
  `default_bom` varchar(180) DEFAULT NULL,
  `inspection_required` varchar(180) DEFAULT NULL,
  `issue_method` varchar(180) DEFAULT NULL,
  `is_asset_item` varchar(180) DEFAULT NULL,
  `is_purchase_item` varchar(180) DEFAULT NULL,
  `is_manufactured_item` varchar(180) DEFAULT NULL,
  `is_sub_contracted_item` varchar(180) DEFAULT NULL,
  `is_stock_item` varchar(180) DEFAULT NULL,
  `is_service_item` varchar(180) DEFAULT NULL,
  `is_sales_item` varchar(180) DEFAULT NULL,
  `is_mrp_item` varchar(180) DEFAULT NULL,
  `abc_category` varchar(180) DEFAULT NULL,
  `has_article_no` varchar(180) DEFAULT NULL,
  `default_warehouse` varchar(180) DEFAULT NULL,
  `minimum_inventory_level` decimal(14,2) DEFAULT NULL,
  `min_order_qty` decimal(14,2) DEFAULT NULL,
  `multiple_order_qty` decimal(14,2) DEFAULT NULL,
  `reorder_level` decimal(14,2) DEFAULT NULL,
  `max_order_qty` decimal(14,2) DEFAULT NULL,
  `max_inventory_allowed` decimal(14,2) DEFAULT NULL,
  `last_inventory_transaction` date DEFAULT NULL,
  `order_method` varchar(180) DEFAULT NULL,
  `lead_time_days` int(11) DEFAULT NULL,
  `purchase_account` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `preferred_supplier` varchar(180) DEFAULT NULL,
  `purchase_uom` varchar(180) DEFAULT NULL,
  `buying_cost` decimal(14,2) DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `last_purchase_rate` decimal(14,2) DEFAULT NULL,
  `last_purchase_uom` varchar(180) DEFAULT NULL,
  `last_purchase_currency` varchar(180) DEFAULT NULL,
  `last_rate_per_uom` decimal(14,2) DEFAULT NULL,
  `last_purchase_transaction` date DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `sales_rate` decimal(14,2) DEFAULT NULL,
  `last_sales_rate` decimal(14,2) DEFAULT NULL,
  `last_sales_transaction` date DEFAULT NULL,
  `old_item_code` varchar(180) DEFAULT NULL,
  `short_description` varchar(180) DEFAULT NULL,
  `item_category` varchar(180) DEFAULT NULL,
  `alternate_description` text,
  `max_discount` decimal(14,2) DEFAULT NULL,
  `sales_bom_old_code` varchar(180) DEFAULT NULL,
  `item_tax_master` varchar(180) DEFAULT NULL,
  `is_sample_item` varchar(180) DEFAULT NULL,
  `has_serial_no` varchar(180) DEFAULT NULL,
  `family_code` varchar(180) DEFAULT NULL,
  `excise_page` varchar(180) DEFAULT NULL,
  `autho_doc_for_lpr` varchar(180) DEFAULT NULL,
  `standard_rate` decimal(14,2) DEFAULT NULL,
  `rol_applicable` varchar(180) DEFAULT NULL,
  `is_pro_applicable` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_category` (`item_category`),
  KEY `old_item_code` (`old_item_code`),
  KEY `sales_bom_old_code` (`sales_bom_old_code`),
  KEY `item_tax_master` (`item_tax_master`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem Attachments Detail`
--

DROP TABLE IF EXISTS `tabItem Attachments Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem Attachments Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `file_name` varchar(180) DEFAULT NULL,
  `file_group` varchar(180) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem Group`
--

DROP TABLE IF EXISTS `tabItem Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem Group` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `group_name` varchar(180) DEFAULT NULL,
  `description` text,
  `show_in_catalogue` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem Specification Detail`
--

DROP TABLE IF EXISTS `tabItem Specification Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem Specification Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `specification` varchar(180) DEFAULT NULL,
  `value` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem Tax`
--

DROP TABLE IF EXISTS `tabItem Tax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem Tax` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `tax_type` varchar(180) DEFAULT NULL,
  `tax_rate` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabItem Tax Master`
--

DROP TABLE IF EXISTS `tabItem Tax Master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabItem Tax Master` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabJournal Voucher`
--

DROP TABLE IF EXISTS `tabJournal Voucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabJournal Voucher` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `voucher_type` varchar(180) DEFAULT NULL,
  `voucher_series` varchar(180) DEFAULT NULL,
  `voucher_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `cheque_no` varchar(180) DEFAULT NULL,
  `cheque_date` date DEFAULT NULL,
  `remark` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `total_debit` decimal(14,2) DEFAULT NULL,
  `total_credit` decimal(14,2) DEFAULT NULL,
  `difference` decimal(14,2) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `pay_amount` decimal(14,2) DEFAULT NULL,
  `pay_to` varchar(180) DEFAULT NULL,
  `in_words` text,
  `pay_to_address` text,
  `cheque_name` varchar(180) DEFAULT NULL,
  `note` text,
  `clearance_date` date DEFAULT NULL,
  `rec_amount` decimal(14,2) DEFAULT NULL,
  `rec_from` varchar(180) DEFAULT NULL,
  `rec_amt_in_words` text,
  `is_opening` varchar(180) DEFAULT NULL,
  `rec_remark` text,
  `pay_remark` text,
  `rec_list` text,
  `is_adv` varchar(180) DEFAULT NULL,
  `supplier_account` varchar(180) DEFAULT NULL,
  `total_tds_amount` decimal(14,2) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  `tds_applicable` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `bill_no` varchar(180) DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `adjusted/cheque_returned` int(3) DEFAULT NULL,
  `adjusted_or_cheque_returned` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `clearance_date` (`clearance_date`),
  KEY `voucher_date` (`voucher_date`),
  KEY `posting_date` (`posting_date`),
  KEY `voucher_type` (`voucher_type`),
  KEY `cheque_no` (`cheque_no`),
  KEY `is_opening` (`is_opening`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`),
  KEY `tds_category` (`tds_category`),
  KEY `tds_applicable` (`tds_applicable`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabJournal Voucher Detail`
--

DROP TABLE IF EXISTS `tabJournal Voucher Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabJournal Voucher Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `balance` varchar(180) DEFAULT NULL,
  `debit` decimal(14,2) DEFAULT NULL,
  `credit` decimal(14,2) DEFAULT NULL,
  `against_voucher` varchar(180) DEFAULT NULL,
  `against_invoice` varchar(180) DEFAULT NULL,
  `against_account` text,
  `is_advance` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `account` (`account`),
  KEY `cost_center` (`cost_center`),
  KEY `against_voucher` (`against_voucher`),
  KEY `against_invoice` (`against_invoice`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead`
--

DROP TABLE IF EXISTS `tabLead`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `lead_name` varchar(180) DEFAULT NULL,
  `lead_owner` varchar(180) DEFAULT NULL,
  `organization` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `item_needed` varchar(180) DEFAULT NULL,
  `address` text,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `telephone` text,
  `work_phone` varchar(180) DEFAULT NULL,
  `home_phone` varchar(180) DEFAULT NULL,
  `cell_number` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `via_campaign` varchar(180) DEFAULT NULL,
  `lead_cost` decimal(14,2) DEFAULT NULL,
  `market_segment` varchar(180) DEFAULT NULL,
  `close_lead` int(3) DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `place` varchar(180) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `by_whom` varchar(180) DEFAULT NULL,
  `interaction` text,
  `lead_status` varchar(180) DEFAULT NULL,
  `contact_by` varchar(180) DEFAULT NULL,
  `contact_date` date DEFAULT NULL,
  `to_discuss` text,
  `todo_item` varchar(180) DEFAULT NULL,
  `last_contact_date` date DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `validated` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `competitor_name` varchar(180) DEFAULT NULL,
  `order_lost_reason` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_address` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `inquiry_type` varchar(180) DEFAULT NULL,
  `type` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `mobile_no` varchar(180) DEFAULT NULL,
  `fax` varchar(180) DEFAULT NULL,
  `website` varchar(180) DEFAULT NULL,
  `industry` varchar(180) DEFAULT NULL,
  `rating` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `event_name` varchar(180) DEFAULT NULL,
  `interested_in` varchar(180) DEFAULT NULL,
  `remark` text,
  `expected_month` varchar(180) DEFAULT NULL,
  `cc_to` varchar(180) DEFAULT NULL,
  `subject` varchar(180) DEFAULT NULL,
  `message` text,
  `sms_message` text,
  `transaction_date` date DEFAULT NULL,
  `campaign_name` varchar(180) DEFAULT NULL,
  `contact_date_ref` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `lead_name` (`lead_name`),
  KEY `lead_owner` (`lead_owner`),
  KEY `organization` (`organization`),
  KEY `status` (`status`),
  KEY `market_segment` (`market_segment`),
  KEY `date` (`date`),
  KEY `company_name` (`company_name`),
  KEY `territory` (`territory`),
  KEY `industry` (`industry`),
  KEY `rating` (`rating`),
  KEY `source` (`source`),
  KEY `expected_month` (`expected_month`),
  KEY `transaction_date` (`transaction_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead Attachment Detail`
--

DROP TABLE IF EXISTS `tabLead Attachment Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead Attachment Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `select_file` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead Item Detail`
--

DROP TABLE IF EXISTS `tabLead Item Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead Item Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `uom` varchar(180) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `amount` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead SMS Detail`
--

DROP TABLE IF EXISTS `tabLead SMS Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead SMS Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `other_mobile_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead Source`
--

DROP TABLE IF EXISTS `tabLead Source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead Source` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `source_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabLead Status`
--

DROP TABLE IF EXISTS `tabLead Status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabLead Status` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMarket Segment`
--

DROP TABLE IF EXISTS `tabMarket Segment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMarket Segment` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `segment_name` varchar(180) DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMaterial Recquisition`
--

DROP TABLE IF EXISTS `tabMaterial Recquisition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMaterial Recquisition` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `transfer_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `Department` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `naming_series` (`naming_series`),
  KEY `transfer_date` (`transfer_date`),
  KEY `posting_date` (`posting_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMaterial Recquisition Detail`
--

DROP TABLE IF EXISTS `tabMaterial Recquisition Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMaterial Recquisition Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `reqd_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMaterial Requisition`
--

DROP TABLE IF EXISTS `tabMaterial Requisition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMaterial Requisition` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `transfer_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `Department` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `naming_series` (`naming_series`),
  KEY `transfer_date` (`transfer_date`),
  KEY `posting_date` (`posting_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMaterial Requisition Detail`
--

DROP TABLE IF EXISTS `tabMaterial Requisition Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMaterial Requisition Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `reqd_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMenu Item`
--

DROP TABLE IF EXISTS `tabMenu Item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMenu Item` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `menu_item_label` varchar(180) DEFAULT NULL,
  `menu_item_type` varchar(180) DEFAULT NULL,
  `link_id` varchar(180) DEFAULT NULL,
  `icon` varchar(180) DEFAULT NULL,
  `parent_menu_item` varchar(180) DEFAULT NULL,
  `has_children` int(3) DEFAULT NULL,
  `parent_menu_item_label` varchar(180) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `criteria_name` varchar(180) DEFAULT NULL,
  `doctype_fields` text,
  `module` varchar(180) DEFAULT NULL,
  `standard` varchar(180) DEFAULT NULL,
  `disabled` varchar(180) DEFAULT NULL,
  `link_content` varchar(180) DEFAULT NULL,
  `onload` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabMenu Item Role`
--

DROP TABLE IF EXISTS `tabMenu Item Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabMenu Item Role` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabModule Def`
--

DROP TABLE IF EXISTS `tabModule Def`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabModule Def` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `module_name` varchar(180) DEFAULT NULL,
  `doctype_list` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabNON-CONFORMANCE REPORT`
--

DROP TABLE IF EXISTS `tabNON-CONFORMANCE REPORT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabNON-CONFORMANCE REPORT` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `is_saved_by_auditor` int(3) DEFAULT NULL,
  `report_ref_no` varchar(180) DEFAULT NULL,
  `report_date` date DEFAULT NULL,
  `department_audited` varchar(180) DEFAULT NULL,
  `area_audited` varchar(180) DEFAULT NULL,
  `scope_of_audit` varchar(180) DEFAULT NULL,
  `date_of_audit` date DEFAULT NULL,
  `non_conformance_in` varchar(180) DEFAULT NULL,
  `non_conformance_details` text,
  `iso_clause_no` varchar(180) DEFAULT NULL,
  `category_of_non_conformance` varchar(180) DEFAULT NULL,
  `auditors` varchar(180) DEFAULT NULL,
  `auditees` varchar(180) DEFAULT NULL,
  `disposal` text,
  `corrective_action` text,
  `head_of_department_name` varchar(180) DEFAULT NULL,
  `signature` varchar(180) DEFAULT NULL,
  `agreed_completion_date` date DEFAULT NULL,
  `corrective_action_completed` varchar(180) DEFAULT NULL,
  `action_taken` text,
  `iso_no` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabOrder Lost Reason`
--

DROP TABLE IF EXISTS `tabOrder Lost Reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabOrder Lost Reason` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `order_lost_reason` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabOrder Reconciliation Detail`
--

DROP TABLE IF EXISTS `tabOrder Reconciliation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabOrder Reconciliation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `sales_order_no` varchar(180) DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `rounded_total` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabOther Charges`
--

DROP TABLE IF EXISTS `tabOther Charges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabOther Charges` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  `is_default` int(3) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `title` (`title`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPCN`
--

DROP TABLE IF EXISTS `tabPCN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPCN` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `pcn_date` date DEFAULT NULL,
  `from` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `product_code` varchar(180) DEFAULT NULL,
  `product_description` text,
  `old_item_code` varchar(180) DEFAULT NULL,
  `drawing_no` varchar(180) DEFAULT NULL,
  `reason` text,
  `validity` varchar(180) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_after` varchar(180) DEFAULT NULL,
  `dcr_no` varchar(180) DEFAULT NULL,
  `dar_no` varchar(180) DEFAULT NULL,
  `iso_no` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPF Detail`
--

DROP TABLE IF EXISTS `tabPF Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPF Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `forecast_date` date DEFAULT NULL,
  `forecast_due_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPO Detail`
--

DROP TABLE IF EXISTS `tabPO Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPO Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `import_rate` decimal(14,2) DEFAULT NULL,
  `billed_qty` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `ref_doc` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `rm_supp_cost` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `received_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `prevdoc_docname` (`prevdoc_docname`),
  KEY `schedule_date` (`schedule_date`),
  KEY `item_code` (`item_code`),
  KEY `item_name` (`item_name`),
  KEY `item_group` (`item_group`),
  KEY `prevdoc_detail_docname` (`prevdoc_detail_docname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPO Material Issue Detail`
--

DROP TABLE IF EXISTS `tabPO Material Issue Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPO Material Issue Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `issue_item_code` varchar(180) DEFAULT NULL,
  `po_item` varchar(180) DEFAULT NULL,
  `issue_warehouse` varchar(180) DEFAULT NULL,
  `issue_description` text,
  `issue_stock_uom` varchar(180) DEFAULT NULL,
  `issue_available_qty` decimal(14,2) DEFAULT NULL,
  `issue_qty` decimal(14,2) DEFAULT NULL,
  `valuation_rate` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPP Detail`
--

DROP TABLE IF EXISTS `tabPP Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPP Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `against_document` varchar(180) DEFAULT NULL,
  `document_no` varchar(180) DEFAULT NULL,
  `document_detail_no` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `document_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `bom_no` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `prevdoc_total_qty` decimal(14,2) DEFAULT NULL,
  `psd_ordered_qty` decimal(14,2) DEFAULT NULL,
  `psd_planned_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_pending_qty` decimal(14,2) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `mrp` int(3) DEFAULT NULL,
  `parent_item` varchar(180) DEFAULT NULL,
  `colour` varchar(180) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  `source_doctype` varchar(180) DEFAULT NULL,
  `source_docname` varchar(180) DEFAULT NULL,
  `source_detail_docname` varchar(180) DEFAULT NULL,
  `prevdoc_reqd_qty` decimal(14,2) DEFAULT NULL,
  `pro_created` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `against_document` (`against_document`),
  KEY `document_date` (`document_date`),
  KEY `delivery_date` (`delivery_date`),
  KEY `confirmation_date` (`confirmation_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPP SO Detail`
--

DROP TABLE IF EXISTS `tabPP SO Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPP SO Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `prevdoc` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `document_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `include_in_plan` int(3) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `mrp` int(3) DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPPW Detail`
--

DROP TABLE IF EXISTS `tabPPW Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPPW Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPR Raw Material Detail`
--

DROP TABLE IF EXISTS `tabPR Raw Material Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPR Raw Material Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `reference_name` varchar(180) DEFAULT NULL,
  `bom_detail_no` varchar(180) DEFAULT NULL,
  `main_item_code` varchar(180) DEFAULT NULL,
  `rm_item_code` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `required_qty` decimal(14,2) DEFAULT NULL,
  `consumed_qty` decimal(14,2) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `description` varchar(180) DEFAULT NULL,
  `current_stock` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPRO Detail`
--

DROP TABLE IF EXISTS `tabPRO Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPRO Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `source_warehouse` varchar(180) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `qty_reqd` decimal(14,6) DEFAULT NULL,
  `issued_qty` decimal(14,6) DEFAULT NULL,
  `consumed_qty` decimal(14,6) DEFAULT NULL,
  `qty_consumed_per_fg` decimal(14,2) DEFAULT NULL,
  `remarks` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPRO PP Detail`
--

DROP TABLE IF EXISTS `tabPRO PP Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPRO PP Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `source_doctype` varchar(180) DEFAULT NULL,
  `source_docname` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `confirm_date` date DEFAULT NULL,
  `qty_reqd` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `update` int(3) DEFAULT NULL,
  `remarks` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPROBLEM REPORTING FORM`
--

DROP TABLE IF EXISTS `tabPROBLEM REPORTING FORM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPROBLEM REPORTING FORM` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `is_report_saved` int(3) DEFAULT NULL,
  `reporting_date` date DEFAULT NULL,
  `target_date` date DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `supervisor` varchar(180) DEFAULT NULL,
  `sign` varchar(180) DEFAULT NULL,
  `product_component_material` varchar(180) DEFAULT NULL,
  `operation` varchar(180) DEFAULT NULL,
  `observation_problem` text,
  `affected_qty` decimal(14,2) DEFAULT NULL,
  `observation_of_problems` text,
  `disposal_action_taken` text,
  `corrective_action_taken` text,
  `preventive_action_taken` text,
  `action_taken_by` varchar(180) DEFAULT NULL,
  `serious` int(3) DEFAULT NULL,
  `moderate` int(3) DEFAULT NULL,
  `minor` int(3) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `responsibility_assigned_to` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `iso_no` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPV Add Tax Detail`
--

DROP TABLE IF EXISTS `tabPV Add Tax Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPV Add Tax Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `add_tax_code` varchar(180) DEFAULT NULL,
  `add_tax_rate` decimal(14,2) DEFAULT NULL,
  `add_amount` decimal(14,2) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPV Ded Tax Detail`
--

DROP TABLE IF EXISTS `tabPV Ded Tax Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPV Ded Tax Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `tax_code` varchar(180) DEFAULT NULL,
  `tax_rate` decimal(14,2) DEFAULT NULL,
  `ded_amount` decimal(14,2) DEFAULT NULL,
  `tds_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPV Detail`
--

DROP TABLE IF EXISTS `tabPV Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPV Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item` varchar(180) DEFAULT NULL,
  `description` text,
  `rate` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `expense_head` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `purchase_order` varchar(180) DEFAULT NULL,
  `po_detail` varchar(180) DEFAULT NULL,
  `purchase_receipt` varchar(180) DEFAULT NULL,
  `pr_detail` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `clear_pending` int(3) DEFAULT NULL,
  `import_rate` decimal(14,2) DEFAULT NULL,
  `rm_supp_cost` decimal(14,2) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `purchase_receipt` (`purchase_receipt`),
  KEY `purchase_order` (`purchase_order`),
  KEY `item` (`item`),
  KEY `item_code` (`item_code`),
  KEY `item_group` (`item_group`),
  KEY `po_detail` (`po_detail`),
  KEY `pr_detail` (`pr_detail`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPacking List Detail Stock Entry`
--

DROP TABLE IF EXISTS `tabPacking List Detail Stock Entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPacking List Detail Stock Entry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `parent_detail_docname` varchar(180) DEFAULT NULL,
  `parent_item` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `stock_entry_no` text,
  `stock_entry_rate` decimal(14,2) DEFAULT NULL,
  `stock_entry_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPage`
--

DROP TABLE IF EXISTS `tabPage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPage` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `content` text,
  `script` text,
  `show_in_menu` int(3) DEFAULT NULL,
  `parent_node` varchar(180) DEFAULT NULL,
  `icon` varchar(180) DEFAULT NULL,
  `menu_index` int(11) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  `standard` varchar(180) DEFAULT NULL,
  `style` text,
  `static_content` text,
  `page_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `module` (`module`),
  KEY `standard` (`standard`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPage Role`
--

DROP TABLE IF EXISTS `tabPage Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPage Role` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPage Visit`
--

DROP TABLE IF EXISTS `tabPage Visit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPage Visit` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `page_name` varchar(180) DEFAULT NULL,
  `date_of_visit` date DEFAULT NULL,
  `new_visit` int(11) DEFAULT NULL,
  `returning_visit` int(11) DEFAULT NULL,
  `country_name` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPartner Target Detail`
--

DROP TABLE IF EXISTS `tabPartner Target Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPartner Target Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `target_amount` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  `achieved_percent` decimal(14,2) DEFAULT NULL,
  `difference` decimal(14,2) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `month` (`month`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `target_amount` (`target_amount`),
  KEY `item_group` (`item_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPayable Voucher`
--

DROP TABLE IF EXISTS `tabPayable Voucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPayable Voucher` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `voucher_series` varchar(180) DEFAULT NULL,
  `voucher_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  `credit_to` varchar(180) DEFAULT NULL,
  `expense_head_main` varchar(180) DEFAULT NULL,
  `cost_center_main` varchar(180) DEFAULT NULL,
  `bill_currency` varchar(180) DEFAULT NULL,
  `po_conversion_rate` decimal(14,2) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `remarks` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `purchase_order_main` varchar(180) DEFAULT NULL,
  `purchase_receipt_main` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `total_taxes` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `total_tax_deducted` decimal(14,2) DEFAULT NULL,
  `total_amount_to_pay` decimal(14,2) DEFAULT NULL,
  `outstanding_amount` decimal(14,2) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `bill_no` varchar(180) DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `is_opening` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `pan_no` varchar(180) DEFAULT NULL,
  `cst_no` varchar(180) DEFAULT NULL,
  `bst_no` varchar(180) DEFAULT NULL,
  `vat_tin_no` varchar(180) DEFAULT NULL,
  `total_adjustment_amount` decimal(14,2) DEFAULT NULL,
  `total_tds_on_voucher` decimal(14,2) DEFAULT NULL,
  `tds_amount_on_advance` decimal(14,2) DEFAULT NULL,
  `total_advance` decimal(14,2) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `manual_tds_entry` int(3) DEFAULT NULL,
  `manual_tax_deduction` int(3) DEFAULT NULL,
  `other_tax_deducted` decimal(14,2) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `voucher_date` (`voucher_date`),
  KEY `posting_date` (`posting_date`),
  KEY `credit_to` (`credit_to`),
  KEY `outstanding_amount` (`outstanding_amount`),
  KEY `due_date` (`due_date`),
  KEY `bill_no` (`bill_no`),
  KEY `bill_date` (`bill_date`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`),
  KEY `is_opening` (`is_opening`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPeriod`
--

DROP TABLE IF EXISTS `tabPeriod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPeriod` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `period_name` varchar(180) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `period_type` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPrice List`
--

DROP TABLE IF EXISTS `tabPrice List`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPrice List` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `adj_percentage` decimal(14,2) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPrint Format`
--

DROP TABLE IF EXISTS `tabPrint Format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPrint Format` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `html` text,
  `module` varchar(180) DEFAULT NULL,
  `standard` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `module` (`module`),
  KEY `standard` (`standard`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduct`
--

DROP TABLE IF EXISTS `tabProduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduct` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `product_name` varchar(180) DEFAULT NULL,
  `show_in_catalogue` int(3) DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `cover_image` varchar(180) DEFAULT NULL,
  `introduction` text,
  `price` decimal(14,6) DEFAULT NULL,
  `shipping_charge` decimal(14,6) DEFAULT NULL,
  `tax` decimal(14,6) DEFAULT NULL,
  `show_price` int(3) DEFAULT NULL,
  `stock_warehouse` varchar(180) DEFAULT NULL,
  `show_stock` int(3) DEFAULT NULL,
  `description` text,
  `product_group` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduct Feature`
--

DROP TABLE IF EXISTS `tabProduct Feature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduct Feature` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `feature_title` varchar(180) DEFAULT NULL,
  `feature_description` text,
  `feature_image` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduct Group`
--

DROP TABLE IF EXISTS `tabProduct Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduct Group` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `product_group` varchar(180) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduct Variance`
--

DROP TABLE IF EXISTS `tabProduct Variance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduct Variance` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `price` decimal(14,2) DEFAULT NULL,
  `show_price` int(3) DEFAULT NULL,
  `variance_image` varchar(180) DEFAULT NULL,
  `image_file` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduct Variant`
--

DROP TABLE IF EXISTS `tabProduct Variant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduct Variant` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `price` decimal(14,2) DEFAULT NULL,
  `show_price` int(3) DEFAULT NULL,
  `variant_image` varchar(180) DEFAULT NULL,
  `image_file` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduction Forecast`
--

DROP TABLE IF EXISTS `tabProduction Forecast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduction Forecast` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `forecast_due_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `amendment_no` int(11) DEFAULT NULL,
  `forecast_name` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `view` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `remarks` text,
  `amendment_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduction Order`
--

DROP TABLE IF EXISTS `tabProduction Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduction Order` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `origin` varchar(180) DEFAULT NULL,
  `prev_doc` varchar(180) DEFAULT NULL,
  `against_document_type` varchar(180) DEFAULT NULL,
  `against_document_no` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `production_item` varchar(180) DEFAULT NULL,
  `description` text,
  `bom_no` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,6) DEFAULT NULL,
  `wip_warehouse` varchar(180) DEFAULT NULL,
  `completed_qty` decimal(14,6) DEFAULT NULL,
  `fg_warehouse` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `remarks` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `consider_sa_items` varchar(180) DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProduction Plan`
--

DROP TABLE IF EXISTS `tabProduction Plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProduction Plan` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `con_exist_stock` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabProfile`
--

DROP TABLE IF EXISTS `tabProfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabProfile` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `enabled` int(3) DEFAULT NULL,
  `send_email_invite` int(3) DEFAULT NULL,
  `escalates_to` varchar(180) DEFAULT NULL,
  `recent_documents` text,
  `first_name` varchar(180) DEFAULT NULL,
  `middle_name` varchar(180) DEFAULT NULL,
  `last_name` varchar(180) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `home_phone` varchar(180) DEFAULT NULL,
  `office_phone` varchar(180) DEFAULT NULL,
  `extension` varchar(180) DEFAULT NULL,
  `cell_no` varchar(180) DEFAULT NULL,
  `last_login` varchar(180) DEFAULT NULL,
  `last_ip` varchar(180) DEFAULT NULL,
  `line_1` varchar(180) DEFAULT NULL,
  `line_2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `district` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `pin` varchar(180) DEFAULT NULL,
  `password` varchar(180) DEFAULT NULL,
  `new_password` varchar(180) DEFAULT NULL,
  `retype_new_password` varchar(180) DEFAULT NULL,
  `file_list` text,
  `password_last_updated` date DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `user_type` varchar(180) DEFAULT NULL,
  `default_type` varchar(180) DEFAULT NULL,
  `supplier_name` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `is_supplier` varchar(180) DEFAULT NULL,
  `is_customer` varchar(180) DEFAULT NULL,
  `is_sales_partner` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_address` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPurchase Common`
--

DROP TABLE IF EXISTS `tabPurchase Common`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPurchase Common` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPurchase Order`
--

DROP TABLE IF EXISTS `tabPurchase Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPurchase Order` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `supplier_ref` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `shipping_order` int(3) DEFAULT NULL,
  `remarks` text,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `payment_terms` text,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `advance_paid` decimal(14,2) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `indent_no` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `under_rule` varchar(180) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `buying_cost_transport` decimal(14,2) DEFAULT NULL,
  `buying_cost_taxes` decimal(14,2) DEFAULT NULL,
  `buying_cost_other` decimal(14,2) DEFAULT NULL,
  `activity_log_text` text,
  `instruction` text,
  `freight` varchar(180) DEFAULT NULL,
  `mode_of_transport` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `order_from` varchar(180) DEFAULT NULL,
  `taxes` varchar(180) DEFAULT NULL,
  `excise_duty` varchar(180) DEFAULT NULL,
  `discount` varchar(180) DEFAULT NULL,
  `requested_by` varchar(180) DEFAULT NULL,
  `required_for` varchar(180) DEFAULT NULL,
  `is_import` varchar(180) DEFAULT NULL,
  `grand_total_import` decimal(14,2) DEFAULT NULL,
  `ref_sq` varchar(180) DEFAULT NULL,
  `approval_status` varchar(180) DEFAULT NULL,
  `billing_status` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `net_total_import` decimal(14,2) DEFAULT NULL,
  `per_received` decimal(14,2) DEFAULT NULL,
  `per_billed` decimal(14,2) DEFAULT NULL,
  `tc_name` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `supplier` (`supplier`),
  KEY `transaction_date` (`transaction_date`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPurchase Receipt`
--

DROP TABLE IF EXISTS `tabPurchase Receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPurchase Receipt` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `posting_time` time DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `lr_no` varchar(180) DEFAULT NULL,
  `lr_date` date DEFAULT NULL,
  `challan_no` varchar(180) DEFAULT NULL,
  `challan_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `remarks` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `purchase_order_no` varchar(180) DEFAULT NULL,
  `rejected_warehouse` varchar(180) DEFAULT NULL,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `buying_cost_transport` decimal(14,2) DEFAULT NULL,
  `buying_cost_taxes` decimal(14,2) DEFAULT NULL,
  `buying_cost_other` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `activity_log_text` text,
  `naming_series` varchar(180) DEFAULT NULL,
  `transporter_name` varchar(180) DEFAULT NULL,
  `security_inward_date` date DEFAULT NULL,
  `security_inward_no.` varchar(180) DEFAULT NULL,
  `bill_no` varchar(180) DEFAULT NULL,
  `submitted_by` varchar(180) DEFAULT NULL,
  `submitted_on` date DEFAULT NULL,
  `pa` varchar(180) DEFAULT NULL,
  `rejection_memo_no` varchar(180) DEFAULT NULL,
  `total_accepted` decimal(14,2) DEFAULT NULL,
  `total_rejected` decimal(14,2) DEFAULT NULL,
  `rejection_reason` text,
  `rejection_memo_date` date DEFAULT NULL,
  `order_from` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `net_total_import` decimal(14,2) DEFAULT NULL,
  `supplier_warehouse` varchar(180) DEFAULT NULL,
  `per_billed` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `is_subcontracted` varchar(180) DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `range` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `posting_date` (`posting_date`),
  KEY `supplier` (`supplier`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `submitted_by` (`submitted_by`),
  KEY `submitted_on` (`submitted_on`),
  KEY `company` (`company`),
  KEY `order_from` (`order_from`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPurchase Receipt Detail`
--

DROP TABLE IF EXISTS `tabPurchase Receipt Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPurchase Receipt Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `schedule_date` date DEFAULT NULL,
  `article_no` text,
  `prevdoc_pending_qty` decimal(14,2) DEFAULT NULL,
  `received_qty` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `rejected_qty` decimal(14,2) DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `accepted_warehouse` varchar(180) DEFAULT NULL,
  `rejected_warehouse` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `import_rate` decimal(14,2) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `billed_qty` decimal(14,2) DEFAULT NULL,
  `returned_qty` decimal(14,2) DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `qa_reported` varchar(180) DEFAULT NULL,
  `tc` varchar(180) DEFAULT NULL,
  `qc` varchar(180) DEFAULT NULL,
  `inspection_date` date DEFAULT NULL,
  `checked_by` varchar(180) DEFAULT NULL,
  `challan_qty` decimal(14,2) DEFAULT NULL,
  `valuation_rate` decimal(14,2) DEFAULT NULL,
  `serial_no` text,
  `clear_pending` int(3) DEFAULT NULL,
  `points_quality` decimal(14,2) DEFAULT NULL,
  `points_certificate` decimal(14,2) DEFAULT NULL,
  `points_price` decimal(14,2) DEFAULT NULL,
  `points_delivery` decimal(14,2) DEFAULT NULL,
  `quality_points` decimal(14,2) DEFAULT NULL,
  `certificate_points` decimal(14,2) DEFAULT NULL,
  `price_points` decimal(14,2) DEFAULT NULL,
  `delivery_points` decimal(14,2) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `rm_supp_cost` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `indent_no` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `prevdoc_docname` (`prevdoc_docname`),
  KEY `item_code` (`item_code`),
  KEY `item_group` (`item_group`),
  KEY `prevdoc_detail_docname` (`prevdoc_detail_docname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabPurchase Tax Detail`
--

DROP TABLE IF EXISTS `tabPurchase Tax Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabPurchase Tax Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `category` varchar(180) DEFAULT NULL,
  `add_deduct_tax` varchar(180) DEFAULT NULL,
  `charge_type` varchar(180) DEFAULT NULL,
  `row_id` varchar(180) DEFAULT NULL,
  `item_wise_tax_detail` text,
  `description` text,
  `account_head` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `tax_amount` decimal(14,2) DEFAULT NULL,
  `total` decimal(14,2) DEFAULT NULL,
  `total_tax_amount` decimal(14,2) DEFAULT NULL,
  `total_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabQA Inspection Report`
--

DROP TABLE IF EXISTS `tabQA Inspection Report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabQA Inspection Report` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `grn_no` varchar(180) DEFAULT NULL,
  `grn_date` date DEFAULT NULL,
  `grn_detail_no` varchar(180) DEFAULT NULL,
  `report_date` date DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `receipt_qty` decimal(14,2) DEFAULT NULL,
  `inspected_by` varchar(180) DEFAULT NULL,
  `sample_size` decimal(14,2) DEFAULT NULL,
  `reference` varchar(180) DEFAULT NULL,
  `report_type` varchar(180) DEFAULT NULL,
  `remarks` text,
  `checked_qty` varchar(180) DEFAULT NULL,
  `accepted_qty` varchar(180) DEFAULT NULL,
  `rejected_qty` varchar(180) DEFAULT NULL,
  `verified_by` varchar(180) DEFAULT NULL,
  `observations` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `purchase_receipt_no` varchar(180) DEFAULT NULL,
  `purchase_receipt_date` date DEFAULT NULL,
  `purchase_receipt_detail_no` varchar(180) DEFAULT NULL,
  `inspection_type` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `delivery_note_date` date DEFAULT NULL,
  `delivery_note_detail` varchar(180) DEFAULT NULL,
  `item_serial_no` varchar(180) DEFAULT NULL,
  `rev_date` date DEFAULT NULL,
  `iso_format_no` varchar(180) DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `grn_no` (`grn_no`),
  KEY `grn_date` (`grn_date`),
  KEY `item_code` (`item_code`),
  KEY `sample_size` (`sample_size`),
  KEY `purchase_receipt_no` (`purchase_receipt_no`),
  KEY `purchase_receipt_date` (`purchase_receipt_date`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabQA Specification Detail`
--

DROP TABLE IF EXISTS `tabQA Specification Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabQA Specification Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `specification` varchar(180) DEFAULT NULL,
  `value` varchar(180) DEFAULT NULL,
  `reading_1` varchar(180) DEFAULT NULL,
  `reading_2` varchar(180) DEFAULT NULL,
  `reading_3` varchar(180) DEFAULT NULL,
  `reading_4` varchar(180) DEFAULT NULL,
  `reading_5` varchar(180) DEFAULT NULL,
  `reading_6` varchar(180) DEFAULT NULL,
  `reading_7` varchar(180) DEFAULT NULL,
  `reading_8` varchar(180) DEFAULT NULL,
  `reading_9` varchar(180) DEFAULT NULL,
  `reading_10` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabQuotation`
--

DROP TABLE IF EXISTS `tabQuotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabQuotation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `inquiry_no` varchar(180) DEFAULT NULL,
  `inquiry_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `quotation_title` varchar(180) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `warranty` varchar(180) DEFAULT NULL,
  `payment_terms` text,
  `opportunity_id` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_ref` varchar(180) DEFAULT NULL,
  `customer_address` text,
  `zone` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `total_commission` decimal(14,2) DEFAULT NULL,
  `intro_note` text,
  `concluding_note` text,
  `internal_note` text,
  `order_loss_reason` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `tc_name` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  `charge` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `final_rate` decimal(14,2) DEFAULT NULL,
  `excise_rate` decimal(14,2) DEFAULT NULL,
  `sales_tax_rate` decimal(14,2) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `total_discount_rate` decimal(14,2) DEFAULT NULL,
  `total_discountc` decimal(14,2) DEFAULT NULL,
  `ref_rate_total` decimal(14,2) DEFAULT NULL,
  `total_discount` decimal(14,2) DEFAULT NULL,
  `approval_status` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `designation` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `gross_profit` decimal(14,2) DEFAULT NULL,
  `gross_profit_percent` decimal(14,2) DEFAULT NULL,
  `enq_no` varchar(180) DEFAULT NULL,
  `enq_det` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `campaign` varchar(180) DEFAULT NULL,
  `order_lost` varchar(180) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  `import_agency_note` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `delivery_date` (`delivery_date`),
  KEY `customer_name` (`customer_name`),
  KEY `territory` (`territory`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `currency` (`currency`),
  KEY `price_list_name` (`price_list_name`),
  KEY `zone` (`zone`),
  KEY `customer_group` (`customer_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabQuotation Detail`
--

DROP TABLE IF EXISTS `tabQuotation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabQuotation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `total_available_qty` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `adj_rate` decimal(14,6) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  `print_rate` decimal(14,2) DEFAULT NULL,
  `print_amt` decimal(14,2) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `colour` varchar(180) DEFAULT NULL,
  `item_tax_rate` text,
  `ref_doc` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `clear_pending` int(3) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `item_name` (`item_name`),
  KEY `item_group` (`item_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRFQ`
--

DROP TABLE IF EXISTS `tabRFQ`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRFQ` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `rfq_date` date DEFAULT NULL,
  `rfq_type` varchar(180) DEFAULT NULL,
  `closing_date` date DEFAULT NULL,
  `rfq_details` text,
  `indent_no` varchar(180) DEFAULT NULL,
  `send_to` varchar(180) DEFAULT NULL,
  `supplier_name` varchar(180) DEFAULT NULL,
  `supplier_type` varchar(180) DEFAULT NULL,
  `from_company` varchar(180) DEFAULT NULL,
  `company_address` text,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `terms_and_conditions` text,
  `rfq_det` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRFQ Detail`
--

DROP TABLE IF EXISTS `tabRFQ Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRFQ Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `indent_no` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `reqd_qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `lead_time_date` date DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `min_order_qty` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `ordered_qty` decimal(14,2) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `product_name` varchar(180) DEFAULT NULL,
  `price` decimal(14,2) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `available_qty` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `indent_no` (`indent_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRV Detail`
--

DROP TABLE IF EXISTS `tabRV Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRV Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `adj_rate` decimal(14,6) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `income_account` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `sales_order` varchar(180) DEFAULT NULL,
  `so_detail` varchar(180) DEFAULT NULL,
  `delivery_note` varchar(180) DEFAULT NULL,
  `dn_detail` varchar(180) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `colour` varchar(180) DEFAULT NULL,
  `item` varchar(180) DEFAULT NULL,
  `item_tax_rate` text,
  `print_rate` decimal(14,2) DEFAULT NULL,
  `print_amt` decimal(14,2) DEFAULT NULL,
  `clear_pending` int(3) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `sales_order` (`sales_order`),
  KEY `delivery_note` (`delivery_note`),
  KEY `item_code` (`item_code`),
  KEY `so_detail` (`so_detail`),
  KEY `dn_detail` (`dn_detail`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRV Tax Detail`
--

DROP TABLE IF EXISTS `tabRV Tax Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRV Tax Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `charge_type` varchar(180) DEFAULT NULL,
  `description` text,
  `account_head` varchar(180) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `total` decimal(14,2) DEFAULT NULL,
  `row_id` varchar(180) DEFAULT NULL,
  `hide` int(3) DEFAULT NULL,
  `tax_amount` decimal(14,2) DEFAULT NULL,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `total_tax_amount` decimal(14,2) DEFAULT NULL,
  `item_wise_tax_detail` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `parenttype` (`parenttype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRating Template`
--

DROP TABLE IF EXISTS `tabRating Template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRating Template` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `template_name` varchar(180) DEFAULT NULL,
  `total_stars` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRating Template Detail`
--

DROP TABLE IF EXISTS `tabRating Template Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRating Template Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `description` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRaw Materials Supplied`
--

DROP TABLE IF EXISTS `tabRaw Materials Supplied`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRaw Materials Supplied` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `po_item` varchar(180) DEFAULT NULL,
  `raw_material` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `source_warehouse` varchar(180) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `ma_valuation_rate` decimal(14,2) DEFAULT NULL,
  `fifo_valuation_rate` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabReceivable Voucher`
--

DROP TABLE IF EXISTS `tabReceivable Voucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabReceivable Voucher` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `voucher_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `debit_to` varchar(180) DEFAULT NULL,
  `income_account_main` varchar(180) DEFAULT NULL,
  `cost_center_main` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `remarks` text,
  `cancel_reason` text,
  `sales_order_main` varchar(180) DEFAULT NULL,
  `delivery_note_main` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `outstanding_amount` decimal(14,2) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `business_associate` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `commission_amount` decimal(14,2) DEFAULT NULL,
  `so_conversion_rate` decimal(14,2) DEFAULT NULL,
  `charge` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `delivery_address` text,
  `zone` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `consinee_address` text,
  `customer_address` text,
  `consignee_address` text,
  `print_label` varchar(180) DEFAULT NULL,
  `po_date` date DEFAULT NULL,
  `po_no` varchar(180) DEFAULT NULL,
  `quotation_no` varchar(180) DEFAULT NULL,
  `bills_through` varchar(180) DEFAULT NULL,
  `billing_address` varchar(180) DEFAULT NULL,
  `billing_name` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `delivery_note_date_main` date DEFAULT NULL,
  `sales_order_date_main` date DEFAULT NULL,
  `mode_of_transport` varchar(180) DEFAULT NULL,
  `vehicle_no` varchar(180) DEFAULT NULL,
  `lr_date` date DEFAULT NULL,
  `lr_no` varchar(180) DEFAULT NULL,
  `transporter_name` varchar(180) DEFAULT NULL,
  `bank_address` text,
  `no_of_packages` varchar(180) DEFAULT NULL,
  `octroi_amount` decimal(14,2) DEFAULT NULL,
  `octroi_receipt_no` varchar(180) DEFAULT NULL,
  `octroi_receipt_date` date DEFAULT NULL,
  `cst_form_type` varchar(180) DEFAULT NULL,
  `concluding_note` text,
  `is_opening` varchar(180) DEFAULT NULL,
  `gross_profit` decimal(14,2) DEFAULT NULL,
  `gross_profit_percent` decimal(14,2) DEFAULT NULL,
  `total_adjustment_amount` decimal(14,2) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `ref_rate_total` decimal(14,2) DEFAULT NULL,
  `total_discount` decimal(14,2) DEFAULT NULL,
  `total_discount_rate` decimal(14,2) DEFAULT NULL,
  `commission_applicable` varchar(180) DEFAULT NULL,
  `discount_rate` decimal(14,2) DEFAULT NULL,
  `cash_discount_rate` decimal(14,2) DEFAULT NULL,
  `net_discount` decimal(14,2) DEFAULT NULL,
  `gross_amt` decimal(14,2) DEFAULT NULL,
  `cash_discount_amt` decimal(14,2) DEFAULT NULL,
  `work_order_value` decimal(14,2) DEFAULT NULL,
  `per_on_ref_rate_total` decimal(14,2) DEFAULT NULL,
  `price_list_value` decimal(14,2) DEFAULT NULL,
  `commission_amt` decimal(14,2) DEFAULT NULL,
  `amount_for_incentive` decimal(14,2) DEFAULT NULL,
  `rate_of_dis_saving` decimal(14,2) DEFAULT NULL,
  `total_incentive` decimal(14,2) DEFAULT NULL,
  `total_commission_amount` decimal(14,2) DEFAULT NULL,
  `total_advance` decimal(14,2) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `voucher_series` varchar(180) DEFAULT NULL,
  `is_emd` varchar(180) DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `campaign` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `due_date` (`due_date`),
  KEY `posting_date` (`posting_date`),
  KEY `debit_to` (`debit_to`),
  KEY `income_account_main` (`income_account_main`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`),
  KEY `is_emd` (`is_emd`),
  KEY `is_opening` (`is_opening`),
  KEY `voucher_date` (`voucher_date`),
  KEY `grand_total` (`grand_total`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabReceiver Detail`
--

DROP TABLE IF EXISTS `tabReceiver Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabReceiver Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `receiver_name` varchar(180) DEFAULT NULL,
  `mobile_no` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRef Rate Detail`
--

DROP TABLE IF EXISTS `tabRef Rate Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRef Rate Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `ref_currency` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `price_list_name` (`price_list_name`),
  KEY `ref_rate` (`ref_rate`),
  KEY `ref_currency` (`ref_currency`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabReport Field Detail`
--

DROP TABLE IF EXISTS `tabReport Field Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabReport Field Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `field_label_fd` varchar(180) DEFAULT NULL,
  `field_type_fd` varchar(180) DEFAULT NULL,
  `options_fd` text,
  `table_name_fd` varchar(180) DEFAULT NULL,
  `field_name_fd` varchar(180) DEFAULT NULL,
  `field_width_fd` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabReport Filter Detail`
--

DROP TABLE IF EXISTS `tabReport Filter Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabReport Filter Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `field_label_fr` varchar(180) DEFAULT NULL,
  `field_type_fr` varchar(180) DEFAULT NULL,
  `options_fr` text,
  `table_name_fr` varchar(180) DEFAULT NULL,
  `field_name_fr` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabReturn Detail`
--

DROP TABLE IF EXISTS `tabReturn Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabReturn Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `detail_name` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` varchar(180) DEFAULT NULL,
  `qty` varchar(180) DEFAULT NULL,
  `returned_qty` varchar(180) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabRole`
--

DROP TABLE IF EXISTS `tabRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabRole` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role_name` varchar(180) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSMS LOG`
--

DROP TABLE IF EXISTS `tabSMS LOG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSMS LOG` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `sms_send_by` varchar(180) DEFAULT NULL,
  `sms_send_to_no` varchar(180) DEFAULT NULL,
  `sending_time` varchar(180) DEFAULT NULL,
  `doctype_name` varchar(180) DEFAULT NULL,
  `document_no` varchar(180) DEFAULT NULL,
  `text_sent` varchar(180) DEFAULT NULL,
  `sending_date` date DEFAULT NULL,
  `sent_by` varchar(180) DEFAULT NULL,
  `sent_to` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSS Deduction Detail`
--

DROP TABLE IF EXISTS `tabSS Deduction Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSS Deduction Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `alias_account_head` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSS Earning Detail`
--

DROP TABLE IF EXISTS `tabSS Earning Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSS Earning Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `alias_account_head` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSalary Slip`
--

DROP TABLE IF EXISTS `tabSalary Slip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSalary Slip` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `year` varchar(180) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `employee_name` varchar(180) DEFAULT NULL,
  `employee_code` varchar(180) DEFAULT NULL,
  `salary_for` varchar(180) DEFAULT NULL,
  `basic_salary` decimal(14,2) DEFAULT NULL,
  `net_basic_salary` varchar(180) DEFAULT NULL,
  `provident_fund` varchar(180) DEFAULT NULL,
  `net_provident_fund` decimal(14,2) DEFAULT NULL,
  `professional_tax` decimal(14,2) DEFAULT NULL,
  `net_professional_tax` decimal(14,2) DEFAULT NULL,
  `total_ot_amount` decimal(14,2) DEFAULT NULL,
  `total_tds` decimal(14,2) DEFAULT NULL,
  `pl` decimal(14,2) DEFAULT NULL,
  `cl` decimal(14,2) DEFAULT NULL,
  `sl` decimal(14,2) DEFAULT NULL,
  `month_days` varchar(180) DEFAULT NULL,
  `working_days` decimal(14,2) DEFAULT NULL,
  `present_days` decimal(14,2) DEFAULT NULL,
  `ot_hours` decimal(14,2) DEFAULT NULL,
  `bank_a/c_no` varchar(180) DEFAULT NULL,
  `cost_center` varchar(180) DEFAULT NULL,
  `l_w_f` decimal(14,2) DEFAULT NULL,
  `advance_amount` decimal(14,2) DEFAULT NULL,
  `total_earning` decimal(14,2) DEFAULT NULL,
  `total_deduction` decimal(14,2) DEFAULT NULL,
  `net_pay` decimal(14,2) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `cost_center` (`cost_center`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales BOM`
--

DROP TABLE IF EXISTS `tabSales BOM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales BOM` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `main_item` varchar(180) DEFAULT NULL,
  `is_active` varchar(180) DEFAULT NULL,
  `new_item_code` varchar(180) DEFAULT NULL,
  `new_item_name` text,
  `new_item_brand` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `price_list` varchar(180) DEFAULT NULL,
  `sales_bom_old_code` varchar(180) DEFAULT NULL,
  `item_tax_master` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales BOM Detail`
--

DROP TABLE IF EXISTS `tabSales BOM Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales BOM Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `is_main_item` varchar(180) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales Order`
--

DROP TABLE IF EXISTS `tabSales Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales Order` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `po_no` varchar(180) DEFAULT NULL,
  `po_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `quotation_no` varchar(180) DEFAULT NULL,
  `quotation_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `price_list_name` varchar(180) DEFAULT NULL,
  `warranty` varchar(180) DEFAULT NULL,
  `payment_terms` text,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_address` text,
  `zone` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `total_commission` decimal(14,2) DEFAULT NULL,
  `note` text,
  `internal_note` text,
  `order_cancellation_reason` text,
  `advance_receipt` decimal(14,2) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  `naming_series` varchar(180) DEFAULT NULL,
  `final_rate` decimal(14,2) DEFAULT NULL,
  `excise_rate` decimal(14,2) DEFAULT NULL,
  `sales_tax_rate` decimal(14,2) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `charge` varchar(180) DEFAULT NULL,
  `ref_rate_total` decimal(14,2) DEFAULT NULL,
  `total_discount` decimal(14,2) DEFAULT NULL,
  `total_discount_rate` decimal(14,2) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `delivery_period` varchar(180) DEFAULT NULL,
  `customer_complaint_no` varchar(180) DEFAULT NULL,
  `mode_of_transport` varchar(180) DEFAULT NULL,
  `billing_address` text,
  `billing_name` varchar(180) DEFAULT NULL,
  `consignee_address` text,
  `indentor_address` text,
  `delivery_to` varchar(180) DEFAULT NULL,
  `bills_through` varchar(180) DEFAULT NULL,
  `enclosed_no` varchar(180) DEFAULT NULL,
  `road_permit` varchar(180) DEFAULT NULL,
  `lr_to` varchar(180) DEFAULT NULL,
  `freight_terms` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `phone_1` varchar(180) DEFAULT NULL,
  `email_1` varchar(180) DEFAULT NULL,
  `total_excise_rate` decimal(14,2) DEFAULT NULL,
  `sales_order_type` varchar(180) DEFAULT NULL,
  `custom_sales_order_no` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `gross_profit` decimal(14,2) DEFAULT NULL,
  `gross_profit_percent` decimal(14,2) DEFAULT NULL,
  `activity_log_text` text,
  `chargeable` varchar(180) DEFAULT NULL,
  `cash_discount_rate` decimal(14,2) DEFAULT NULL,
  `cash_discount_amt` decimal(14,2) DEFAULT NULL,
  `work_order_value` decimal(14,2) DEFAULT NULL,
  `per_on_ref_rate_total` decimal(14,2) DEFAULT NULL,
  `price_list_value` decimal(14,2) DEFAULT NULL,
  `commission_amt` decimal(14,2) DEFAULT NULL,
  `amount_for_incentive` decimal(14,2) DEFAULT NULL,
  `rate_of_dis_saving` decimal(14,2) DEFAULT NULL,
  `total_incentive` decimal(14,2) DEFAULT NULL,
  `total_commission_amount` decimal(14,2) DEFAULT NULL,
  `net_discount` decimal(14,2) DEFAULT NULL,
  `gross_amt` decimal(14,2) DEFAULT NULL,
  `discount_rate` decimal(14,2) DEFAULT NULL,
  `commission_applicable` varchar(180) DEFAULT NULL,
  `baseline` decimal(14,2) DEFAULT NULL,
  `diff_baseline_discount` decimal(14,2) DEFAULT NULL,
  `saving_factor` decimal(14,2) DEFAULT NULL,
  `inquiry_no` varchar(180) DEFAULT NULL,
  `inquiry_date` date DEFAULT NULL,
  `concluding_note` text,
  `tc_name` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `per_delivered` varchar(180) DEFAULT NULL,
  `per_billed` varchar(180) DEFAULT NULL,
  `source` varchar(180) DEFAULT NULL,
  `campaign` varchar(180) DEFAULT NULL,
  `credit_control_approval` varchar(180) DEFAULT NULL,
  `address1` varchar(180) DEFAULT NULL,
  `submitted_on` date DEFAULT NULL,
  `submitted_by` varchar(180) DEFAULT NULL,
  `remarks_from_marketing` text,
  `remarks_from_factory` text,
  `remarks_mrktg` text,
  `remarks_factory` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `customer_name` (`customer_name`),
  KEY `territory` (`territory`),
  KEY `sales_partner` (`sales_partner`),
  KEY `city` (`city`),
  KEY `department` (`department`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`),
  KEY `state` (`state`),
  KEY `quotation_no` (`quotation_no`),
  KEY `address1` (`address1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales Order Detail`
--

DROP TABLE IF EXISTS `tabSales Order Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales Order Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` text,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `stock_uom` varchar(180) DEFAULT NULL,
  `total_available_qty` decimal(14,2) DEFAULT NULL,
  `reserved_warehouse` varchar(180) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `ref_rate` decimal(14,2) DEFAULT NULL,
  `adj_rate` decimal(14,6) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `billed_qty` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `planned_qty` decimal(14,2) DEFAULT NULL,
  `produced_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `print_amt` decimal(14,2) DEFAULT NULL,
  `print_rate` decimal(14,2) DEFAULT NULL,
  `formica` varchar(180) DEFAULT NULL,
  `colour` varchar(180) DEFAULT NULL,
  `reasons` varchar(180) DEFAULT NULL,
  `defect_details` text,
  `chargeable` varchar(180) DEFAULT NULL,
  `alternate_description` int(3) DEFAULT NULL,
  `item_tax_rate` text,
  `item_group` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `confirmation_date` date DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  `delivered_qty` decimal(14,2) DEFAULT NULL,
  `projected_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `reasons` (`reasons`),
  KEY `chargeable` (`chargeable`),
  KEY `prevdoc_docname` (`prevdoc_docname`),
  KEY `brand` (`brand`),
  KEY `item_group` (`item_group`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales Partner`
--

DROP TABLE IF EXISTS `tabSales Partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales Partner` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `partner_name` varchar(180) DEFAULT NULL,
  `partner_type` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `area_code` varchar(180) DEFAULT NULL,
  `mobile` varchar(180) DEFAULT NULL,
  `person` varchar(180) DEFAULT NULL,
  `telephone` varchar(180) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `address` text,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `partner_type` (`partner_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales Person`
--

DROP TABLE IF EXISTS `tabSales Person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales Person` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `sales_person` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `mobile_no` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `sales_person` (`sales_person`),
  KEY `territory` (`territory`),
  KEY `country` (`country`),
  KEY `state` (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSales Team`
--

DROP TABLE IF EXISTS `tabSales Team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSales Team` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `sales_person` varchar(180) DEFAULT NULL,
  `allocated_percentage` decimal(14,2) DEFAULT NULL,
  `allocated_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `sales_person` (`sales_person`),
  KEY `parenttype` (`parenttype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSearch Criteria`
--

DROP TABLE IF EXISTS `tabSearch Criteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSearch Criteria` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `disabled` int(3) DEFAULT NULL,
  `criteria_name` varchar(180) DEFAULT NULL,
  `doc_type` varchar(180) DEFAULT NULL,
  `filters` text,
  `columns` text,
  `parent_doc_type` varchar(180) DEFAULT NULL,
  `add_cond` text,
  `add_col` text,
  `add_tab` text,
  `dis_filters` text,
  `group_by` varchar(180) DEFAULT NULL,
  `graph_series` varchar(180) DEFAULT NULL,
  `graph_values` varchar(180) DEFAULT NULL,
  `report_script` text,
  `server_script` text,
  `module` varchar(180) DEFAULT NULL,
  `description` text,
  `sort_by` varchar(180) DEFAULT NULL,
  `sort_order` varchar(180) DEFAULT NULL,
  `custom_query` text,
  `standard` varchar(180) DEFAULT NULL,
  `page_len` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `criteria_name` (`criteria_name`),
  KEY `standard` (`standard`),
  KEY `module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSerial No`
--

DROP TABLE IF EXISTS `tabSerial No`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSerial No` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `serial_no` varchar(180) DEFAULT NULL,
  `make` varchar(180) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `pr_no` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `is_cancelled` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `serial_no` (`serial_no`),
  KEY `purchase_date` (`purchase_date`),
  KEY `purchase_rate` (`purchase_rate`),
  KEY `pr_no` (`pr_no`),
  KEY `delivery_note_no` (`delivery_note_no`),
  KEY `status` (`status`),
  KEY `is_cancelled` (`is_cancelled`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSeries`
--

DROP TABLE IF EXISTS `tabSeries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSeries` (
  `name` varchar(40) DEFAULT NULL,
  `current` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSeries Detail`
--

DROP TABLE IF EXISTS `tabSeries Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSeries Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `series` varchar(180) DEFAULT NULL,
  `remove` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabService Order`
--

DROP TABLE IF EXISTS `tabService Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabService Order` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `service_quotation_no` varchar(180) DEFAULT NULL,
  `service_quotation_date` date DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `po_no` varchar(180) DEFAULT NULL,
  `po_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `order_type` varchar(180) DEFAULT NULL,
  `others_detail` varchar(180) DEFAULT NULL,
  `payment_terms` text,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_ref` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `customer_address` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `total_commission` decimal(14,2) DEFAULT NULL,
  `note` text,
  `internal_note` text,
  `concluding_note` text,
  `order_cancellation_reason` text,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `charge` varchar(180) DEFAULT NULL,
  `advance_receipt` decimal(14,2) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `tc_name` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `customer_name` (`customer_name`),
  KEY `territory` (`territory`),
  KEY `sales_partner` (`sales_partner`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabService Order Detail`
--

DROP TABLE IF EXISTS `tabService Order Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabService Order Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `serial_no` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `no_of_visit` int(11) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `item_tax_rate` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `serial_no` (`serial_no`),
  KEY `item_code` (`item_code`),
  KEY `start_date` (`start_date`),
  KEY `end_date` (`end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabService Quotation`
--

DROP TABLE IF EXISTS `tabService Quotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabService Quotation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `inquiry_no` varchar(180) DEFAULT NULL,
  `inquiry_date` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `quotation_title` varchar(180) DEFAULT NULL,
  `quotation_type` varchar(180) DEFAULT NULL,
  `others_detail` varchar(180) DEFAULT NULL,
  `sub_category` varchar(180) DEFAULT NULL,
  `quotation_stages` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `currency` varchar(180) DEFAULT NULL,
  `conversion_rate` decimal(14,2) DEFAULT NULL,
  `quotation_sent_mode` varchar(180) DEFAULT NULL,
  `approved_by` varchar(180) DEFAULT NULL,
  `payment_terms` text,
  `customer_name` varchar(180) DEFAULT NULL,
  `customer_ref` varchar(180) DEFAULT NULL,
  `customer_address` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `territory` varchar(180) DEFAULT NULL,
  `customer_group` varchar(180) DEFAULT NULL,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `sales_partner` varchar(180) DEFAULT NULL,
  `commission_rate` decimal(14,2) DEFAULT NULL,
  `total_commission` decimal(14,2) DEFAULT NULL,
  `intro_note` text,
  `concluding_note` text,
  `internal_note` text,
  `order_loss_reason` text,
  `charge` varchar(180) DEFAULT NULL,
  `net_total` decimal(14,2) DEFAULT NULL,
  `other_charges_total` decimal(14,2) DEFAULT NULL,
  `grand_total` decimal(14,2) DEFAULT NULL,
  `rounded_total` decimal(14,2) DEFAULT NULL,
  `in_words` varchar(180) DEFAULT NULL,
  `grand_total_export` decimal(14,2) DEFAULT NULL,
  `rounded_total_export` decimal(14,2) DEFAULT NULL,
  `in_words_export` varchar(180) DEFAULT NULL,
  `tc_name` varchar(180) DEFAULT NULL,
  `quote_received_by_customer` varchar(180) DEFAULT NULL,
  `customer_mobile_no` varchar(180) DEFAULT NULL,
  `message` text,
  `file_list` text,
  `approval_status` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `status` (`status`),
  KEY `transaction_date` (`transaction_date`),
  KEY `customer_name` (`customer_name`),
  KEY `customer_address` (`customer_address`),
  KEY `territory` (`territory`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabService Quotation Detail`
--

DROP TABLE IF EXISTS `tabService Quotation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabService Quotation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `serial_no` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `make` varchar(180) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `amc_start_date` date DEFAULT NULL,
  `amc_end_date` date DEFAULT NULL,
  `no_of_visit` int(11) DEFAULT NULL,
  `qty` decimal(14,2) DEFAULT NULL,
  `basic_rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `item_tax_rate` text,
  `brand` varchar(180) DEFAULT NULL,
  `export_rate` decimal(14,2) DEFAULT NULL,
  `export_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `serial_no` (`serial_no`),
  KEY `item_code` (`item_code`),
  KEY `amc_start_date` (`amc_start_date`),
  KEY `no_of_visit` (`no_of_visit`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabService Schedule`
--

DROP TABLE IF EXISTS `tabService Schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabService Schedule` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `service_type` varchar(180) DEFAULT NULL,
  `against_docname` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSessions`
--

DROP TABLE IF EXISTS `tabSessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSessions` (
  `user` varchar(40) DEFAULT NULL,
  `sid` varchar(120) DEFAULT NULL,
  `sessiondata` longtext,
  `ipaddress` varchar(16) DEFAULT NULL,
  `lastupdate` datetime DEFAULT NULL,
  KEY `sid` (`sid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSingles`
--

DROP TABLE IF EXISTS `tabSingles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSingles` (
  `doctype` varchar(40) DEFAULT NULL,
  `field` varchar(40) DEFAULT NULL,
  `value` text,
  KEY `doctype` (`doctype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSite Map Detail`
--

DROP TABLE IF EXISTS `tabSite Map Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSite Map Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `label` varchar(180) DEFAULT NULL,
  `type` varchar(180) DEFAULT NULL,
  `doc_name` varchar(180) DEFAULT NULL,
  `roles` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSpecification Detail`
--

DROP TABLE IF EXISTS `tabSpecification Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSpecification Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `specification` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabState`
--

DROP TABLE IF EXISTS `tabState`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabState` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `state_name` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabStock Entry`
--

DROP TABLE IF EXISTS `tabStock Entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabStock Entry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `transfer_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `posting_time` time DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `from_warehouse` varchar(180) DEFAULT NULL,
  `to_warehouse` varchar(180) DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `transporter` varchar(180) DEFAULT NULL,
  `is_excisable_goods` varchar(180) DEFAULT NULL,
  `excisable_goods` varchar(180) DEFAULT NULL,
  `under_rule` varchar(180) DEFAULT NULL,
  `remarks` text,
  `cancel_reason` varchar(180) DEFAULT NULL,
  `prepared_by` varchar(180) DEFAULT NULL,
  `received_by` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `Department` varchar(180) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  `issue_to` varchar(180) DEFAULT NULL,
  `ref_no` varchar(180) DEFAULT NULL,
  `activity_log_text` text,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `purpose` varchar(180) DEFAULT NULL,
  `delivery_note_no` varchar(180) DEFAULT NULL,
  `purchase_receipt_no` varchar(180) DEFAULT NULL,
  `process` varchar(180) DEFAULT NULL,
  `production_order` varchar(180) DEFAULT NULL,
  `fg_completed_qty` decimal(14,2) DEFAULT NULL,
  `consumption_per_fg` decimal(14,2) DEFAULT NULL,
  `total_consumption_amt` decimal(14,2) DEFAULT NULL,
  `consumption_amt_per_fg` decimal(14,2) DEFAULT NULL,
  `sa_production` varchar(180) DEFAULT NULL,
  `packing_details_se` decimal(14,2) DEFAULT NULL,
  `charge` varchar(180) DEFAULT NULL,
  `excise_duty_paid` decimal(14,2) DEFAULT NULL,
  `excise_duty_in_words` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `transfer_date` (`transfer_date`),
  KEY `posting_date` (`posting_date`),
  KEY `to_warehouse` (`to_warehouse`),
  KEY `naming_series` (`naming_series`),
  KEY `Department` (`Department`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabStock Entry Detail`
--

DROP TABLE IF EXISTS `tabStock Entry Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabStock Entry Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `description` text,
  `actual_qty` varchar(180) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `transfer_qty` decimal(14,2) DEFAULT NULL,
  `incoming_rate` decimal(14,2) DEFAULT NULL,
  `remark` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `detail_name` varchar(180) DEFAULT NULL,
  `s_warehouse` varchar(180) DEFAULT NULL,
  `t_warehouse` varchar(180) DEFAULT NULL,
  `fg_item` int(3) DEFAULT NULL,
  `total_qty` decimal(14,2) DEFAULT NULL,
  `reqd_qty` decimal(14,2) DEFAULT NULL,
  `stock_entry_no` text,
  `stock_entryno` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `actual_qty` (`actual_qty`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabStock Entry Other Charges Tax`
--

DROP TABLE IF EXISTS `tabStock Entry Other Charges Tax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabStock Entry Other Charges Tax` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `charge_type` varchar(180) DEFAULT NULL,
  `item_wise_tax_detail` text,
  `description` text,
  `row_id` varchar(180) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `tax_amount` decimal(14,2) DEFAULT NULL,
  `total` decimal(14,2) DEFAULT NULL,
  `hide` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `parenttype` (`parenttype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabStock Ledger Entry`
--

DROP TABLE IF EXISTS `tabStock Ledger Entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabStock Ledger Entry` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `posting_time` time DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `voucher_type` varchar(180) DEFAULT NULL,
  `voucher_no` varchar(180) DEFAULT NULL,
  `voucher_detail_no` varchar(180) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `incoming_rate` decimal(14,2) DEFAULT NULL,
  `bin_aqat` decimal(14,2) DEFAULT NULL,
  `ma_rate` decimal(14,2) DEFAULT NULL,
  `fcfs_rate` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `is_cancelled` varchar(180) DEFAULT NULL,
  `is_stock_entry` varchar(180) DEFAULT NULL,
  `warehouse_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `item_code` (`item_code`),
  KEY `warehouse` (`warehouse`),
  KEY `posting_date` (`posting_date`),
  KEY `transaction_date` (`transaction_date`),
  KEY `voucher_type` (`voucher_type`),
  KEY `voucher_no` (`voucher_no`),
  KEY `is_cancelled` (`is_cancelled`),
  KEY `is_stock_entry` (`is_stock_entry`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabStock Reconciliation`
--

DROP TABLE IF EXISTS `tabStock Reconciliation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabStock Reconciliation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `reconciliation_date` date DEFAULT NULL,
  `next_step` varchar(180) DEFAULT NULL,
  `remark` text,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `file_list` text,
  `posting_time` time DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSupplier`
--

DROP TABLE IF EXISTS `tabSupplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSupplier` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `supplier_name` varchar(180) DEFAULT NULL,
  `supplier_group` varchar(180) DEFAULT NULL,
  `supplier_type` varchar(180) DEFAULT NULL,
  `supplier_status` varchar(180) DEFAULT NULL,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `website` varchar(180) DEFAULT NULL,
  `address` text,
  `contact_person_name` varchar(180) DEFAULT NULL,
  `phone_1` varchar(180) DEFAULT NULL,
  `phone_2` varchar(180) DEFAULT NULL,
  `mobile_1` varchar(180) DEFAULT NULL,
  `telephone` text,
  `fax_1` varchar(180) DEFAULT NULL,
  `email_1` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  `pan_no` varchar(180) DEFAULT NULL,
  `cst_no` varchar(180) DEFAULT NULL,
  `bst_no` varchar(180) DEFAULT NULL,
  `vat_tin_no` varchar(180) DEFAULT NULL,
  `authorization_document` varchar(180) DEFAULT NULL,
  `last_purchase_order` varchar(180) DEFAULT NULL,
  `credit_days` varchar(180) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `address_line1` (`address_line1`),
  KEY `address_line2` (`address_line2`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSupplier Quotation`
--

DROP TABLE IF EXISTS `tabSupplier Quotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSupplier Quotation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `ref_no` varchar(180) DEFAULT NULL,
  `quotation_date` date DEFAULT NULL,
  `quotation_status` varchar(180) DEFAULT NULL,
  `approval_status` varchar(180) DEFAULT NULL,
  `supplier_name` varchar(180) DEFAULT NULL,
  `supplier_address` text,
  `activity_log_text` text,
  `contact_person` varchar(180) DEFAULT NULL,
  `contact_no` varchar(180) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `terms_and_conditions` text,
  `net_total` decimal(14,2) DEFAULT NULL,
  `enq_no` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `supplier` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSupplier Quotation Detail`
--

DROP TABLE IF EXISTS `tabSupplier Quotation Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSupplier Quotation Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `rfq_no` varchar(180) DEFAULT NULL,
  `prevdoc_docname` varchar(180) DEFAULT NULL,
  `prevdoc_detail_docname` varchar(180) DEFAULT NULL,
  `item_code` varchar(180) DEFAULT NULL,
  `item_name` varchar(180) DEFAULT NULL,
  `brand` varchar(180) DEFAULT NULL,
  `description` text,
  `qty` decimal(14,2) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  `stock_uom` varchar(180) DEFAULT NULL,
  `stock_qty` decimal(14,2) DEFAULT NULL,
  `lead_time_date` date DEFAULT NULL,
  `schedule_date` date DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `min_order_qty` decimal(14,2) DEFAULT NULL,
  `pending_qty` decimal(14,2) DEFAULT NULL,
  `ordered_qty` decimal(14,2) DEFAULT NULL,
  `actual_qty` decimal(14,2) DEFAULT NULL,
  `cleared_qty` decimal(14,2) DEFAULT NULL,
  `prevdoc_doctype` varchar(180) DEFAULT NULL,
  `purchase_rate` decimal(14,2) DEFAULT NULL,
  `page_break` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSupplier TDS Category Detail`
--

DROP TABLE IF EXISTS `tabSupplier TDS Category Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSupplier TDS Category Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabSupplier Type`
--

DROP TABLE IF EXISTS `tabSupplier Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabSupplier Type` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `supplier_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTC Detail`
--

DROP TABLE IF EXISTS `tabTC Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTC Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `terms` varchar(180) DEFAULT NULL,
  `description` text,
  `page_break` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTCN`
--

DROP TABLE IF EXISTS `tabTCN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTCN` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `tcn_date` date DEFAULT NULL,
  `from` varchar(180) DEFAULT NULL,
  `department` varchar(180) DEFAULT NULL,
  `product_code` varchar(180) DEFAULT NULL,
  `product_description` text,
  `old_item_code` varchar(180) DEFAULT NULL,
  `drawing_no` varchar(180) DEFAULT NULL,
  `reason` varchar(180) DEFAULT NULL,
  `validity` varchar(180) DEFAULT NULL,
  `proposed_modification` text,
  `request_accepted` text,
  `dcr_no` varchar(180) DEFAULT NULL,
  `dar_no` varchar(180) DEFAULT NULL,
  `valid_for_qty` decimal(14,2) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `iso_no` varchar(180) DEFAULT NULL,
  `company_name` varchar(180) DEFAULT NULL,
  `company_abbr` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`),
  KEY `fiscal_year` (`fiscal_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Category`
--

DROP TABLE IF EXISTS `tabTDS Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Category` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `category_name` varchar(180) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Category Account`
--

DROP TABLE IF EXISTS `tabTDS Category Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Category Account` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `account_type` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `account_head` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Payment`
--

DROP TABLE IF EXISTS `tabTDS Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Payment` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `tds_category` varchar(180) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `posting_date` date DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `pan_no` varchar(180) DEFAULT NULL,
  `tan_no` varchar(180) DEFAULT NULL,
  `cheque_no` varchar(180) DEFAULT NULL,
  `bsr_code` varchar(180) DEFAULT NULL,
  `challan_no` varchar(180) DEFAULT NULL,
  `remarks` text,
  `total_main_tds` decimal(14,2) DEFAULT NULL,
  `total_surcharge` decimal(14,2) DEFAULT NULL,
  `total_edu_cess` decimal(14,2) DEFAULT NULL,
  `total_sh_edu_cess` decimal(14,2) DEFAULT NULL,
  `total_tds` decimal(14,2) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  `date_of_recipt` date DEFAULT NULL,
  `amended_from` varchar(180) DEFAULT NULL,
  `amendment_date` date DEFAULT NULL,
  `date_of_receipt` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `company` (`company`),
  KEY `from_date` (`from_date`),
  KEY `to_date` (`to_date`),
  KEY `tds_category` (`tds_category`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Payment Detail`
--

DROP TABLE IF EXISTS `tabTDS Payment Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Payment Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `voucher_no` varchar(180) DEFAULT NULL,
  `party_name` varchar(180) DEFAULT NULL,
  `amount_paid` decimal(14,2) DEFAULT NULL,
  `date_of_payment` date DEFAULT NULL,
  `tds_main` decimal(14,2) DEFAULT NULL,
  `surcharge` decimal(14,2) DEFAULT NULL,
  `edu_cess` decimal(14,2) DEFAULT NULL,
  `sh_edu_cess` decimal(14,2) DEFAULT NULL,
  `total_tax_amount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Rate Chart`
--

DROP TABLE IF EXISTS `tabTDS Rate Chart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Rate Chart` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `applicable_from` date DEFAULT NULL,
  `applicable_to` date DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTDS Rate Detail`
--

DROP TABLE IF EXISTS `tabTDS Rate Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTDS Rate Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `category` varchar(180) DEFAULT NULL,
  `slab_from` decimal(14,2) DEFAULT NULL,
  `slab_to` decimal(14,2) DEFAULT NULL,
  `rate` decimal(14,2) DEFAULT NULL,
  `surcharge` decimal(14,2) DEFAULT NULL,
  `ec` decimal(14,2) DEFAULT NULL,
  `shec` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTable Mapper Detail`
--

DROP TABLE IF EXISTS `tabTable Mapper Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTable Mapper Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `from_table` varchar(180) DEFAULT NULL,
  `to_table` varchar(180) DEFAULT NULL,
  `from_field` varchar(180) DEFAULT NULL,
  `to_field` varchar(180) DEFAULT NULL,
  `match_id` int(11) DEFAULT NULL,
  `validation_logic` text,
  `reference_doctype_key` varchar(180) DEFAULT NULL,
  `reference_key` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTarget Detail`
--

DROP TABLE IF EXISTS `tabTarget Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTarget Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `target_amount` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `achieved_percent` decimal(14,2) DEFAULT NULL,
  `difference` decimal(14,2) DEFAULT NULL,
  `distribution_id` varchar(180) DEFAULT NULL,
  `target_qty` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `from_date` (`from_date`),
  KEY `to_date` (`to_date`),
  KEY `target_amount` (`target_amount`),
  KEY `item_group` (`item_group`),
  KEY `month` (`month`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `target_qty` (`target_qty`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTechnician`
--

DROP TABLE IF EXISTS `tabTechnician`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTechnician` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `technician_name` varchar(180) DEFAULT NULL,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTechnician Attendance`
--

DROP TABLE IF EXISTS `tabTechnician Attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTechnician Attendance` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `technician_name` varchar(180) DEFAULT NULL,
  `location` varchar(180) DEFAULT NULL,
  `naming_series` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTechnician Attendance Detail`
--

DROP TABLE IF EXISTS `tabTechnician Attendance Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTechnician Attendance Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `date_of_visit` date DEFAULT NULL,
  `customer` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `chargeable` varchar(180) DEFAULT NULL,
  `purpose` varchar(180) DEFAULT NULL,
  `complaint_no` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `expenses_claim` varchar(180) DEFAULT NULL,
  `amount` decimal(14,2) DEFAULT NULL,
  `remark` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTerms And Conditions`
--

DROP TABLE IF EXISTS `tabTerms And Conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTerms And Conditions` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `title` varchar(180) DEFAULT NULL,
  `is_default` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTerritory`
--

DROP TABLE IF EXISTS `tabTerritory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTerritory` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `territory_name` varchar(180) DEFAULT NULL,
  `old_territory_name` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `zone` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `territory_manager` varchar(180) DEFAULT NULL,
  `cell_no` varchar(180) DEFAULT NULL,
  `phone` varchar(180) DEFAULT NULL,
  `email_id` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `city` (`city`),
  KEY `country` (`country`),
  KEY `state` (`state`),
  KEY `zone` (`zone`),
  KEY `territory_manager` (`territory_manager`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTerritory Target Detail`
--

DROP TABLE IF EXISTS `tabTerritory Target Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTerritory Target Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `item_group` varchar(180) DEFAULT NULL,
  `month` varchar(180) DEFAULT NULL,
  `fiscal_year` varchar(180) DEFAULT NULL,
  `target_amount` decimal(14,2) DEFAULT NULL,
  `actual` decimal(14,2) DEFAULT NULL,
  `achieved_percent` decimal(14,2) DEFAULT NULL,
  `difference` decimal(14,2) DEFAULT NULL,
  `forecasts` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `month` (`month`),
  KEY `fiscal_year` (`fiscal_year`),
  KEY `target_amount` (`target_amount`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTestDT`
--

DROP TABLE IF EXISTS `tabTestDT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTestDT` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `test_data` varchar(180) DEFAULT NULL,
  `test_link` varchar(180) DEFAULT NULL,
  `test_currency` decimal(14,2) DEFAULT NULL,
  `test_date` date DEFAULT NULL,
  `test_select` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `test_currency` (`test_currency`),
  KEY `test_date` (`test_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTestTabDT`
--

DROP TABLE IF EXISTS `tabTestTabDT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTestTabDT` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `test` varchar(180) DEFAULT NULL,
  `DocType` varchar(180) DEFAULT NULL,
  `link` varchar(180) DEFAULT NULL,
  `testtab_curr` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTicket`
--

DROP TABLE IF EXISTS `tabTicket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTicket` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `subject` varchar(180) DEFAULT NULL,
  `type` varchar(180) DEFAULT NULL,
  `status` varchar(180) DEFAULT NULL,
  `reason` text,
  `document_num` varchar(180) DEFAULT NULL,
  `ticket_by` varchar(180) DEFAULT NULL,
  `ticket_by_email` varchar(180) DEFAULT NULL,
  `description` text,
  `priority` varchar(180) DEFAULT NULL,
  `senders_name` varchar(180) DEFAULT NULL,
  `senders_email` varchar(180) DEFAULT NULL,
  `senders_contact_no` varchar(180) DEFAULT NULL,
  `senders_company` varchar(180) DEFAULT NULL,
  `response` text,
  `allocated_to` varchar(180) DEFAULT NULL,
  `assignee_email` varchar(180) DEFAULT NULL,
  `scheduled_date` date DEFAULT NULL,
  `resolution_date` date DEFAULT NULL,
  `first_creation_flag` int(11) DEFAULT NULL,
  `second_creation_flag` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `priority` (`priority`),
  KEY `senders_name` (`senders_name`),
  KEY `scheduled_date` (`scheduled_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTicket Response Detail`
--

DROP TABLE IF EXISTS `tabTicket Response Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTicket Response Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `response` text,
  `response_by` varchar(180) DEFAULT NULL,
  `response_date` date DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabToDo Item`
--

DROP TABLE IF EXISTS `tabToDo Item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabToDo Item` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `description` text,
  `date` date DEFAULT NULL,
  `priority` varchar(180) DEFAULT NULL,
  `reference_type` varchar(180) DEFAULT NULL,
  `reference_name` varchar(180) DEFAULT NULL,
  `checked` int(3) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTransfer Account`
--

DROP TABLE IF EXISTS `tabTransfer Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTransfer Account` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `server` varchar(180) DEFAULT NULL,
  `path` varchar(180) DEFAULT NULL,
  `account` varchar(180) DEFAULT NULL,
  `admin_password` varchar(180) DEFAULT NULL,
  `transfer` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTransfer Module`
--

DROP TABLE IF EXISTS `tabTransfer Module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTransfer Module` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `module` varchar(180) DEFAULT NULL,
  `transfer` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTransporter`
--

DROP TABLE IF EXISTS `tabTransporter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTransporter` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `transporter_name` varchar(180) DEFAULT NULL,
  `address_line1` varchar(180) DEFAULT NULL,
  `address_line2` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `pincode` varchar(180) DEFAULT NULL,
  `transporter_rate` decimal(14,2) DEFAULT NULL,
  `phone_no` varchar(180) DEFAULT NULL,
  `email_address` varchar(180) DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabTweet`
--

DROP TABLE IF EXISTS `tabTweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabTweet` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `by` varchar(180) DEFAULT NULL,
  `comment` text,
  `tag` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUOM`
--

DROP TABLE IF EXISTS `tabUOM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUOM` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `uom_name` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUOM Conversion Detail`
--

DROP TABLE IF EXISTS `tabUOM Conversion Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUOM Conversion Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `uom` varchar(180) DEFAULT NULL,
  `conversion_factor` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUser Setting-Profile`
--

DROP TABLE IF EXISTS `tabUser Setting-Profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUser Setting-Profile` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `profile_id` varchar(180) DEFAULT NULL,
  `enabled` int(3) DEFAULT NULL,
  `first_name` varchar(180) DEFAULT NULL,
  `last_name` varchar(180) DEFAULT NULL,
  `email` varchar(180) DEFAULT NULL,
  `phone` varchar(180) DEFAULT NULL,
  `changed` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUser Setting-Role Permission`
--

DROP TABLE IF EXISTS `tabUser Setting-Role Permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUser Setting-Role Permission` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `doc_type` varchar(180) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `read` int(3) DEFAULT NULL,
  `write` int(3) DEFAULT NULL,
  `create` int(3) DEFAULT NULL,
  `submit` int(3) DEFAULT NULL,
  `cancel` int(3) DEFAULT NULL,
  `amend` int(3) DEFAULT NULL,
  `match` varchar(180) DEFAULT NULL,
  `remove_permission` int(3) DEFAULT NULL,
  `changed` int(3) DEFAULT NULL,
  `new_perm` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUser Setting-Role User`
--

DROP TABLE IF EXISTS `tabUser Setting-Role User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUser Setting-Role User` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `profile_id` varchar(180) DEFAULT NULL,
  `remove` int(3) DEFAULT NULL,
  `changed` int(3) DEFAULT NULL,
  `is_new` int(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabUserRole`
--

DROP TABLE IF EXISTS `tabUserRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabUserRole` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `role` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWarehouse`
--

DROP TABLE IF EXISTS `tabWarehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWarehouse` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `warehouse_name` varchar(180) DEFAULT NULL,
  `warehouse_type` varchar(180) DEFAULT NULL,
  `company` varchar(180) DEFAULT NULL,
  `phone_no` int(11) DEFAULT NULL,
  `address_line_1` varchar(180) DEFAULT NULL,
  `address_line_2` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  `state` varchar(180) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `mobile_no` varchar(180) DEFAULT NULL,
  `country` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWarehouse Type`
--

DROP TABLE IF EXISTS `tabWarehouse Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWarehouse Type` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `warehouse_type` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `warehouse_type` (`warehouse_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWeb Visitor`
--

DROP TABLE IF EXISTS `tabWeb Visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWeb Visitor` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `ip_address` varchar(180) DEFAULT NULL,
  `country_name` varchar(180) DEFAULT NULL,
  `city` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWiki History`
--

DROP TABLE IF EXISTS `tabWiki History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWiki History` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `reference` varchar(180) DEFAULT NULL,
  `version_no` varchar(180) DEFAULT NULL,
  `revision` int(11) DEFAULT NULL,
  `editor` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWiki Page`
--

DROP TABLE IF EXISTS `tabWiki Page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWiki Page` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `page_name` varchar(180) DEFAULT NULL,
  `editor` text,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWorkflow Action Detail`
--

DROP TABLE IF EXISTS `tabWorkflow Action Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWorkflow Action Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `action_field` varchar(180) DEFAULT NULL,
  `action_value` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWorkflow Rule`
--

DROP TABLE IF EXISTS `tabWorkflow Rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWorkflow Rule` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `rule_name` varchar(180) DEFAULT NULL,
  `rule_status` varchar(180) DEFAULT NULL,
  `select_form` varchar(180) DEFAULT NULL,
  `rule_priority` int(11) DEFAULT NULL,
  `extra_condition` text,
  `message` text,
  `raise_exception` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `rule_status` (`rule_status`),
  KEY `select_form` (`select_form`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWorkflow Rule Detail`
--

DROP TABLE IF EXISTS `tabWorkflow Rule Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWorkflow Rule Detail` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `rule_field` varchar(180) DEFAULT NULL,
  `operator` varchar(180) DEFAULT NULL,
  `value` varchar(180) DEFAULT NULL,
  `comparing_field` varchar(180) DEFAULT NULL,
  `message` varchar(180) DEFAULT NULL,
  `exception` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabWorkstation`
--

DROP TABLE IF EXISTS `tabWorkstation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabWorkstation` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `workstation_name` varchar(180) DEFAULT NULL,
  `warehouse` varchar(180) DEFAULT NULL,
  `description` text,
  `capacity` varchar(180) DEFAULT NULL,
  `capacity_units` varchar(180) DEFAULT NULL,
  `hour_rate_labour` decimal(14,2) DEFAULT NULL,
  `hour_rate_electricity` decimal(14,2) DEFAULT NULL,
  `hour_rate_consumable` decimal(14,2) DEFAULT NULL,
  `hour_rate_rent` decimal(14,2) DEFAULT NULL,
  `overhead` decimal(14,2) DEFAULT NULL,
  `hour_rate` decimal(14,2) DEFAULT NULL,
  `prev_hour_rate` decimal(14,2) DEFAULT NULL,
  `bom_list` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabZone`
--

DROP TABLE IF EXISTS `tabZone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabZone` (
  `name` varchar(120) NOT NULL,
  `creation` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `modified_by` varchar(40) DEFAULT NULL,
  `owner` varchar(40) DEFAULT NULL,
  `docstatus` int(1) DEFAULT '0',
  `parent` varchar(120) DEFAULT NULL,
  `parentfield` varchar(120) DEFAULT NULL,
  `parenttype` varchar(120) DEFAULT NULL,
  `idx` int(8) DEFAULT NULL,
  `zone_name` varchar(180) DEFAULT NULL,
  `zone_manager` varchar(180) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-09-30 16:19:34
