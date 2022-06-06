import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JsondialogComponent } from './jsondialog.component';

describe('JsondialogComponent', () => {
  let component: JsondialogComponent;
  let fixture: ComponentFixture<JsondialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JsondialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(JsondialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
