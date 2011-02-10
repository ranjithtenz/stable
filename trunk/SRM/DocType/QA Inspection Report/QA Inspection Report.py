class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist

  def get_item_specification_details(self):
    self.doc.clear_table(self.doclist, 'qa_specification_details')
    specification = sql("select specification, value from `tabItem Specification Detail` where parent = '%s' order by idx" % (self.doc.item_code))
    for d in specification:
      child = addchild(self.doc, 'qa_specification_details', 'QA Specification Detail', 1, self.doclist)
      child.specification = d[0]
      child.value = d[1]
      child.status = 'Accepted'

  def on_submit(self):
    if self.doc.purchase_receipt_no:
      sql("update `tabPurchase Receipt Detail` set qa_no = '%s' where parent = '%s' and item_code = '%s'" % (self.doc.name, self.doc.purchase_receipt_no, self.doc.item_code))

    # make feed
    get_obj('Feed Control').make_feed('submitted', self.doc.doctype, self.doc.name)


  def on_cancel(self):
    if self.doc.purchase_receipt_no:
      sql("update `tabPurchase Receipt Detail` set qa_no = '' where parent = '%s' and item_code = '%s'" % (self.doc.purchase_receipt_no, self.doc.item_code))

    # make feed
    get_obj('Feed Control').make_feed('cancelled', self.doc.doctype, self.doc.name)

  # on update
  def on_update(self):
    obj = get_obj('Feed Control', 'Feed Control')
    
    if not self.doc.creation:
      obj.make_feed('created', self.doc.doctype, self.doc.name)
    else:
      obj.make_feed('modified', self.doc.doctype, self.doc.name)