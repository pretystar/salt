import { Component, OnInit, Input, Inject } from '@angular/core';
import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource} from '@angular/material/tree';
// import {BehaviorSubject} from 'rxjs';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
// import {MatDialogModule} from '@angular/material/dialog';


export class treenode {
  children: treenode[];
  name: string;
  type: any;
}

@Component({
  selector: 'ngx-jsondialog',
  templateUrl: './jsondialog.component.html',
  styleUrls: ['./jsondialog.component.scss']
})
export class JsondialogComponent implements OnInit {
  // @Input() data;
  nestedTreeControl: NestedTreeControl<treenode>;
  nestedDataSource: MatTreeNestedDataSource<treenode>;

  onNoClick(): void {
    this.dialogRef.close();
  }

  constructor(    
      public dialogRef: MatDialogRef<JsondialogComponent>,
      @Inject(MAT_DIALOG_DATA) public data: any
    ) {
      this.nestedTreeControl = new NestedTreeControl<treenode>(this._getChildren);
      this.nestedDataSource = new MatTreeNestedDataSource();
      this.nestedDataSource.data = this.buildFileTree(data,0)
  }

  hasNestedChild = (_: number, nodeData: treenode) => !nodeData.type;

  private _getChildren = (node: treenode) => node.children;
  // constructor() { }

  ngOnInit(): void {
  }
  buildFileTree(obj: object, level: number): treenode[] {
    return Object.keys(obj).reduce<treenode[]>((accumulator, key) => {
      const value = obj[key];
      const node = new treenode();
      node.name = key;

      if (value != null) {
        if (typeof value === 'object') {
          node.children = this.buildFileTree(value, level + 1);
        } else {
          node.type = value;
        }
      }

      return accumulator.concat(node);
    }, []);
  }
}
